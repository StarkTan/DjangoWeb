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
    print("Connect with the result code " + str(rc))
    client.subscribe('/usi/device/config/#')
    client.subscribe('/usi/device/data/#')

# 接收、处理mqtt消息
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload)

    if float(json.loads(msg.payload)['version']) <=1.1:
        dev_msg = {
            'sn': 'test00001',
            'name': 'loacl_test',
            'version': '1.2',
            'config': {
                'switch_led1': 'on',
                'slider_led2_0_100': 60,
            }
        }
        client.publish('/usi/cloud/config/test00001', json.dumps(dev_msg), qos=1)


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