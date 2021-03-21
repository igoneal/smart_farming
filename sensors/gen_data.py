import pandas as pd
import time
import paho.mqtt.client as mqtt
import socket
import pickle
import os


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class BrokerCom:
    def __init__(self, user, pw, ip, sub_topic):
        self.user = user
        self.pw = pw
        self.ip = ip
        self.port = 1883
        self.topic = sub_topic
        self.client = mqtt.Client()
        self.client.username_pw_set(self.user, self.pw)
        self.client.connect(self.ip, self.port, 60)
        self.mec_ip = ip_address()
        self.run = 1

    def on_connect(self, connect_client, userdata, flags, rc):
        print("Connected with Code :" + str(rc))
        # Subscribe Topic from here
        connect_client.subscribe(self.topic)

    def on_message(self, message_client, userdata, msg):
        print(f'Topic received: {msg.topic}')
        topic_recv = msg.topic
        data = pickle.loads(msg.payload)
        print(data)
        save_data(data)

    def publish(self, topic, data):
        self.client.publish(topic, data)

    def broker_loop(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()
        while True:
            if self.run == 0:
                self.client.loop_stop()
                self.client.disconnect()
                break

    def __del__(self):
        print('Broker Communication Object Deleted!')


def display_data():
    os.system('clear')
    topic = input('Enter Topic: ')
    ip = input('Enter Broker ip: ')
    br = BrokerCom(user='mec', pw='password', ip=ip, sub_topic=topic)
    df = pd.read_csv('data.csv')
    for i in range(df.shape[0]):
        row = dict(df.iloc[i, :])
        print(row)
        r = pickle.dumps(row)
        br.publish(topic=topic, data=r)
        time.sleep(1)


def save_data(data):
    pass


if __name__ == '__main__':
    display_data()
