import paho.mqtt.client as mqtt

from mqtt_router import MQTTRouter

router = MQTTRouter()


@router.add("telemetry/devices/<str:streaming_key>/<int:count>/meta")
def handle_meta(message, context, streaming_key=None, count=None):
    print("Received meta '%s' with count '%d' from device '%s'" % (message, count, streaming_key))


def on_message(client, userdata, message):
    router.route(message.topic, message, context={"client": client, "userdata": userdata})


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()


if __name__ == "__main__":
    main()
