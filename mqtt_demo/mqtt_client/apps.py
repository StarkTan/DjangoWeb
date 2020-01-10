import sys
import json
from threading import Thread, Timer
from django.apps import AppConfig
import paho.mqtt.client as mqtt
import time
# from device.models import Device
cfg_pre = '/usi/device/config/'
data_pre = '/usi/device/data/'
pub_pre = '/usi/cloud/config/'
client = mqtt.Client()


class MqttClientConfig(AppConfig):
    name = 'mqtt_client'
    Device = None

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)

    # 在App加载完成后会被调用一次
    def ready(self):
        if len(sys.argv)>1 and sys.argv[1] == 'runserver':
            from device.models import Device  # 需要应用加载完了，才能从Django环境中获取到数据库ORM
            MqttClientConfig.Device = Device
            MqttClientConfig.mqtt_run()
            MqttClientConfig.sync_device()

    @staticmethod
    def on_connect(client, userdata, flag, rc):
        print("Connect with the result code " + str(rc))
        client.subscribe(cfg_pre + '#')
        client.subscribe(data_pre + '#')

    @staticmethod
    def mqtt_run():
        client.on_connect = MqttClientConfig.on_connect
        client.on_message = MqttClientConfig.on_message
        # broker = '127.0.0.1'  # 47.52.203.253
        client.username_pw_set('mqtttest', '123456')
        client.reconnect_delay_set(min_delay=1, max_delay=2000)
        mqttthread = Thread(target=MqttClientConfig.mqtt_function)
        mqttthread.start()

    @staticmethod
    def on_message(client, userdata, msg):
        Device = MqttClientConfig.Device
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
                            client.publish(pub_pre + sn, json.dumps(device.pub_msg()), qos=1)
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
    @staticmethod
    def mqtt_function():
        broker = '47.52.203.253'
        not_conn = True
        while not_conn:
            try:
                client.connect(broker, 2016, 600)
                not_conn = False
            except:
                print('mqtt conn failed! try again')
                time.sleep(3)
        # 使用loop_start 可以避免阻塞Django进程，使用loop_forever()可能会阻塞系统进程
        client.loop_start()
        # client.loop()
        # client.loop_forever() 有掉线重连功能
        # client.loop_forever()
        
    @staticmethod
    def sync_device():
        timer = Timer(5, MqttClientConfig.sync_device)
        timer.setDaemon(True)
        timer.start()
        if client.is_connected():
            print('sync device config')
            un_confirm_dev = MqttClientConfig.Device.objects.filter(confirm=False)
            for dev in un_confirm_dev:
                sn = dev.id
                client.publish(pub_pre + sn, json.dumps(dev.pub_msg()), qos=1)
        else:
            print('mqtt is not connected')



