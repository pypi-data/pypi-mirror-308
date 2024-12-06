# MQTT Router

MQTT Router is a simple to use client-agnostic mqtt message router.

You can use mqtt-router to declare mqtt message handlers using a simple and minimal
python decorator syntax.

mqtt-router helps you extract parameters from topics that contains wildcards and cast
those parameters into the desired python data type.


## Getting Started
Install the library using Pip:
```
pip install mqtt-router
```


## Using mqtt-router
```python
from mqtt_router import MQTTRouter


router = MQTTRouter()

# Subscribe to telemetry/#/#/data
@router.add("telemetry/<str:streaming_key>/<int:count>/data")
def handle_meta(message, context, streaming_key=None, count=None):
    ...


# Subscribe to telemetry/+
@router.add("telemetry/<path:rest>")
def handle_rest(message, context, rest=None):
    ...


def on_message(message, topic, client, userdata):
    router.route(topic, message, context={"client": client, "userdata": userdata})


mqtt_client.on_message = on_message
```