import re
import string

from .converters import DEFAULT_CONVERTERS

_PATH_PARAMETER_COMPONENT_RE = r"<(?:(?P<converter>[^>:]+):)?(?P<parameter>[^>]+)>"


class MQTTRouter:
    def __init__(self):
        self.routes = {}

    def add(self, path):
        def wrapper(func):
            regex, converters = self._route_to_regex(path)
            if self.routes.get(regex):
                self.routes[regex]["handlers"].append(func)
            else:
                self.routes[regex] = {
                    "handlers": [func],
                    "converters": converters,
                }
            return func

        return wrapper

    def route(self, topic, message, context=None):
        for regex, defs in self.routes.items():
            match, _, params = self._match(re.compile(regex, 0), topic, defs.get("converters", {}))
            if match is not None:
                for handler in defs["handlers"]:
                    handler(message, context, **params)

    def _route_to_regex(self, route):
        """
        Convert a path pattern into a regular expression. Return the regular
        expression and a dictionary mapping the capture names to the converters.
        For example, 'foo/<int:pk>' returns '^foo\\/(?P<pk>[0-9]+)'
        and {'pk': <mqtt_router.converters.IntConverter>}.
        """
        original_route = route
        parts = ["^"]
        converters = {}
        while True:
            match = re.compile(_PATH_PARAMETER_COMPONENT_RE, 0).search(route)
            if not match:
                parts.append(re.escape(route))
                break
            elif not set(match.group()).isdisjoint(string.whitespace):
                raise ValueError("URL route '%s' cannot contain whitespace in angle brackets " "<…>." % original_route)
            parts.append(re.escape(route[: match.start()]))
            route = route[match.end() :]
            parameter = match["parameter"]
            if not parameter.isidentifier():
                raise ValueError(
                    "URL route '%s' uses parameter name %r which isn't a valid "
                    "Python identifier." % (original_route, parameter)
                )
            raw_converter = match["converter"]
            if raw_converter is None:
                # If a converter isn't specified, the default is `str`.
                raw_converter = "str"
            try:
                converter = DEFAULT_CONVERTERS[raw_converter]
            except KeyError as e:
                raise ValueError("URL route %r uses invalid converter %r." % (original_route, raw_converter)) from e
            converters[parameter] = converter
            parts.append("(?P<" + parameter + ">" + converter.regex + ")")
        return "".join(parts), converters

    def _match(self, regex, path, converters):
        match = regex.search(path)
        if not match:
            return None, (), {}
        # non-named groups are not allowed so args are ignored.
        kwargs = match.groupdict()
        for key, value in kwargs.items():
            converter = converters[key]
            try:
                kwargs[key] = converter.to_python(value)
            except ValueError:
                return None
        return path[match.end() :], (), kwargs
