import time
import os
import paho.mqtt.client as mqtt
import socket
import pickle
import sqlite3


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
        self.mec_ip = ip_address()
        self.run = 1

    def on_connect(self, connect_client, userdata, flags, rc):
        print("Connected with Code :" + str(rc))
        # Subscribe Topic from here
        connect_client.subscribe(self.topic)

    def on_message(self, message_client, userdata, msg):
        print(f'Topic received: {msg.topic}')
        topic_recv = msg.topic
        m = pickle.loads(msg.payload)
        print('here')
        print(m)

    def publish(self, topic, data):
        self.client.publish(topic, data)

    def broker_loop(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.username_pw_set(self.user, self.pw)
        self.client.connect(self.ip, self.port, 60)
        self.client.loop_start()
        while True:
            if self.run == 0:
                self.client.loop_stop()
                self.client.disconnect()
                break

    def __del__(self):
        print('Broker Communication Object Deleted!')


class Yield:
    conn = sqlite3.connect('yield.db')
    c = conn.cursor()
    c.execute(""" CREATE TABLE crop_data(
        moisture, rainfall, humidity, temperature, crop_yield
        )""")
    conn.commit()
    conn.close()


def initialization():
    ip = input('Enter Broker ip: ')
    topic = input('Enter Topic: ')
    br = BrokerCom(user='admin', pw='password', ip=ip, sub_topic=topic)
    try:
        br.broker_loop()
    except KeyboardInterrupt:
        br.run = 0


if __name__ == '__main__':
    os.system('clear')
    initialization()
