import paho.mqtt.client as mqtt
import json
sn = 'test00002'
cfg_pub = '/usi/device/config/%s' % sn
cfg_sub = '/usi/cloud/config/%s' %sn
# 配置文件
dev_msg = {
    'sn': sn,
    'name': 'loacl_test',
    'version': '1.1',
    'config':{
    'switch_led1': 'on',
    'slider_led2_0_100': 50,
    }
}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    if rc == 0:
        # 连接成功时上报状态
        client.publish(cfg_pub, json.dumps(dev_msg), qos=1)


def on_message(client, userdata, msg):
    print(msg.payload)
    payload = msg.payload
    cloud_msg = json.loads(payload)
    # 检查版本
    local_ver = dev_msg['version'].split('.')
    cloud_ver = cloud_msg['version'].split('.')
    if int(local_ver[0]) > int(cloud_ver[0]):
        # 本地版本较高
        client.publish(cfg_pub, json.dumps(dev_msg), qos=1)
        return
    if int(local_ver[0]) == int(cloud_ver[0]) and int(local_ver[1]) >= int(cloud_ver[1]):
        # 本地版本较高
        client.publish(cfg_pub, json.dumps(dev_msg), qos=1)
        return
    dev_msg['version'] = cloud_msg['version']
    dev_cfg = dev_msg['config']
    cloud_cfg = cloud_msg['config']
    for key in dev_cfg.keys():
        if key in cloud_cfg.keys() and not dev_cfg[key]==cloud_cfg[key]:
            value = cloud_cfg[key]
            arr = key.split('_')
            if arr[0].lower() == 'switch':
                if not value =='on' and dev_cfg[key]=='on':
                    continue
                if not value == 'on':
                    value = 'off'
                print('set %s status to %s'%(arr[0], value))
            elif arr[0].lower() == 'slider':
                print('set %s data to %s' % (arr[0], value))
            dev_cfg[key] = value
    print('current config: '+str(dev_cfg))
    client.publish(cfg_pub, json.dumps(dev_msg), qos=1)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('127.0.0.1', 1883, 600) # 600为keepalive的时间间隔
client.subscribe(cfg_sub, qos=1)
client.loop_forever()  # 一直保持连接