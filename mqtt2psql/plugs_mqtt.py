import paho.mqtt.client as mqtt
import re
import json
import typing as ty
from mqtt2psql.data import PlugSensor, PlugState


PARSE_TOPIC = re.compile("^plugs/([^/]+)/tele/([^/]+)$")


class PlugsMqtt:
    def __init__(self, 
                host: str, 
                port: int, 
                user: str, 
                password: str, 
                consumer: ty.Callable[[str, PlugSensor or PlugState], None]
    ):
        self.consumer = consumer
        self.client: mqtt.Client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect_fail = self.on_connect_fail
        self.client.on_disconnect = self.on_disconnect
        self.client.username_pw_set(user, password)
        self.client.connect(host, port)
        self.client.subscribe("plugs/#")

    def on_message(self, client, data, message):
        msg = PARSE_TOPIC.match(message.topic)
        if msg is not None and msg.groups()[1] in ("STATE", "SENSOR"):
            payload = json.loads(message.payload)
            if msg.groups()[1] == "STATE":
                state = PlugState.from_json(payload)
            else:
                state = PlugSensor.from_json(payload)
            
            self.consumer(msg.groups()[0], state)

    def on_connect_fail(self):
        raise RuntimeError("Failed to connect")

    def on_disconnect(self):
        raise RuntimeError("Client disconnected")

    def run(self):
        self.client.loop_forever()