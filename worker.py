import paho.mqtt.client as mqtt
import json
import pandas as pd
from datetime import datetime
import os

FILE = "motor_log.csv"

if not os.path.exists(FILE):
    df = pd.DataFrame(columns=[
        "timestamp",
        "rpm",
        "voltage",
        "current",
        "pwm"
    ])
    df.to_csv(FILE,index=False)


def on_message(client, userdata, msg):

    print("Pesan diterima!")
    print(msg.topic)
    print(msg.payload.decode())

    data = json.loads(
        msg.payload.decode()
    )

    row = {
        "timestamp": datetime.now(),
        "rpm": data["rpm"],
        "voltage": data["voltage"],
        "current": data["current"],
        "pwm": data["pwm"]
    }

    pd.DataFrame([row]).to_csv(
        FILE,
        mode='a',
        header=False,
        index=False
    )

    print(row)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION1
)

client.username_pw_set(
    "arduino",
    "123456"
)

client.connect(
    "localhost",
    1883
)

client.subscribe("motor/data")
print("Subscribe ke motor/data berhasil")

client.on_message = on_message

print("Worker Running...")
client.loop_forever()