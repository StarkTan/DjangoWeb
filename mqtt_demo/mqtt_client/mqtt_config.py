import os, sys
import django
import paho.mqtt.client as mqtt
from threading import Thread
import time
import json
os.environ.setdefault('DJANGO_SETTING_MODULE', 'mqtt_demo.settings')
django.setup()

from device.models import Device

client = mqtt.Client(client_id="test", clean_session=False)
cfg_pre = '/usi/device/config/'
data_pre = '/usi/device/data/'
pub_pre = '/usi/cloud/config/'

# 建立mqtt连接
def on_connect(client, userdata, flag, rc):
    print("Connect with the result code " + str(rc))
    client.subscribe(cfg_pre+'#')
    client.subscribe(data_pre+'#')

# 接收、处理mqtt消息
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload)
    topic = msg.topic
    if topic.startswith(cfg_pre):
        sn = topic.replace(cfg_pre, '')
        dev_msg = json.loads(msg.payload)
        try:
            if not sn == dev_msg['sn']:
                print('found error msg topic %s payload %s' % (msg.topic, msg.topic))
            else:
                res = Device.objects.filter(id=sn)
                if res.count() == 0:
                    print('dev_msg not exist')
                    device = Device()
                    device.id = sn
                    device.name = dev_msg['name']
                    device.config = json.dumps(dev_msg['config'])
                    device.version = dev_msg['version']
                    device.save()
                    print('dev_msg saved')
                else:
                    device = res[0]
                    local_ver = dev_msg['version'].split('.')
                    cloud_ver = device.version.split('.')
                    if int(local_ver[0]) > int(cloud_ver[0]) or \
                            (int(local_ver[0]) == int(cloud_ver[0]) and int(local_ver[1]) >= int(cloud_ver[1])):
                        device.config = json.dumps(dev_msg['config'])
                        device.confirm = True
                        device.version = dev_msg['version']
                        device.save()
                        print('dev_msg updated')
                    else:
                        device.confirm = False
                        device.save()
                        client.publish(pub_pre+sn, json.dumps(device.pub_msg()), qos=1)
                        print('confirm dev_config')
        except Exception as e:
            print(e)
    elif topic.startswith(data_pre):
        sn = topic.replace(data_pre, '')
        dev_msg = json.loads(msg.payload)
        if not sn == dev_msg['sn']:
            print('found error msg topic %s payload %s' % (msg.topic, msg.topic))
        else:
            print('handle data')
    else:
        print('found unknown msg topic %s payload %s' % (msg.topic, msg.topic))


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
    # broker = '127.0.0.1'  # 47.52.203.253
    broker = '47.52.203.253'
    client.username_pw_set('mqtttest', '123456')
    client.reconnect_delay_set(min_delay=1, max_delay=2000)
    client.connect(broker, 2016, 600)
    mqttthread = Thread(target=mqtt_function)
    mqttthread.start()
    mqtt_function()
mqtt_run()