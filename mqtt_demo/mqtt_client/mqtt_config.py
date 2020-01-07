import os, sys
import django
import paho.mqtt.client as mqtt
from threading import Thread
import time
import json
os.environ.setdefault('DJANGO_SETTING_MODULE', 'mqtt_demo.settings')
django.setup()

client = mqtt.Client(client_id="test", clean_session=False)


# 建立mqtt连接
def on_connect(client, userdata, flag, rc):
    print(time.time())
    print("Connect with the result code " + str(rc))
    client.subscribe('test/#')


# 接收、处理mqtt消息
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload)


# mqtt客户端启动函数
def mqtt_function():
    global client
    # 使用loop_start 可以避免阻塞Django进程，使用loop_forever()可能会阻塞系统进程
    client.loop_start()
    # client.loop()
    # client.loop_forever() 有掉线重连功能
    # client.loop_forever()


def mqtt_run():
    client.on_connect = on_connect
    client.on_message = on_message
    broker = '127.0.0.1'
    client.connect(broker, 1883, 600)
    client.username_pw_set('user', 'user')
    client.reconnect_delay_set(min_delay=1, max_delay=2000)
    mqttthread = Thread(target=mqtt_function)
    mqttthread.start()
    mqtt_function()
mqtt_run()