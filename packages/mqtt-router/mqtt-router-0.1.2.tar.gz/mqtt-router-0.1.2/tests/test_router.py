from unittest import TestCase
from unittest.mock import Mock

from mqtt_router import MQTTRouter
from mqtt_router.converters import IntConverter, PathConverter, StringConverter


class RouterTestCase(TestCase):
    def test_add(self):
        handle_meta = Mock()
        router = MQTTRouter()
        router.add("telemetry/devices/<streaming_key>/<int:count>/meta")(handle_meta)

        regex = "^telemetry/devices/(?P<streaming_key>[^/]+)/(?P<count>[0-9]+)/meta"
        self.assertIn(regex, router.routes)

        route = router.routes[regex]
        self.assertEqual(len(route["handlers"]), 1)
        self.assertEqual(route["handlers"][0], handle_meta)

        self.assertIn("streaming_key", route["converters"])
        self.assertIsInstance(route["converters"]["streaming_key"], StringConverter)

        self.assertIn("count", route["converters"])
        self.assertIsInstance(route["converters"]["count"], IntConverter)

    def test_add_path_wildcard(self):
        handle_meta = Mock()
        router = MQTTRouter()
        router.add("telemetry/<path:rest>")(handle_meta)

        regex = "^telemetry/(?P<rest>.+)"
        self.assertIn(regex, router.routes)

        route = router.routes[regex]
        self.assertEqual(len(route["handlers"]), 1)
        self.assertEqual(route["handlers"][0], handle_meta)

        self.assertIn("rest", route["converters"])
        self.assertIsInstance(route["converters"]["rest"], PathConverter)

    def test_route(self):
        handle_message = Mock()
        router = MQTTRouter()
        router.add("telemetry/devices/<streaming_key>/<int:count>/meta")(handle_message)

        topic = "telemetry/devices/key/1234/meta"
        message = "Hello there!"
        context = {"extra": "extra data"}
        router.route(topic, message, context=context)

        handle_message.assert_called_once_with(message, context, streaming_key="key", count=1234)

    def test_route_path_wildcard(self):
        handle_message = Mock()
        router = MQTTRouter()
        router.add("telemetry/<path:rest>")(handle_message)

        topic = "telemetry/devices/key/1234/data"
        message = "Hello there!"
        context = {"extra": "extra data"}
        router.route(topic, message, context=context)

        handle_message.assert_called_once_with(message, context, rest="devices/key/1234/data")
