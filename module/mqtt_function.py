import os, sys
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'auction.settings')
django.setup()

import paho.mqtt.client as mqtt
from threading import Thread
from api import models

import time
import json

# 建立mqtt连接
def on_connect(client, userdata, flag, rc):
    print("Connect with the result code " + str(rc))
    client.subscribe('data/recerive', qcs=0)

# 接收 处理mqtt消息
def on_message(client, userdata, msg):
    out = msg.payload.decode('utf-8')
    # print("topic:"+msg.topic)
    # print(out)  string类型
    # out = json.loads(out)

    # 收到消息后执行任务
    if msg.topic == 'data/receive':
        # 处理model层业务
        # 增
        #  obj = models.MqttData(topic=msg.topic, msg=out)
        # obj,save()
        # 查
        # data = models.MqttData.objects.all()
        # print(data)
        # 改
        models.MqttData.objects.filter(topic=msg.topic).update(msg=out)

# mqtt客户端启动函数
def mqttfunction():
    global client
    # 使用loop_start 可以避免阻塞django的进程，使用loop_forever()可能会阻塞系统进程
    # client.loop_start()
    # client.loop_forever() # 有断线重连的功能
    client.loop_forever(retry_first_connection=True)

client = mqtt.Client(client_id="test", clean_session=False)


# 启动函数
def mqtt_run():
    client.on_connect = on_connect()
    client.on_message = on_message()
    # 绑定mqtt服务器地址
    broker = '139.9.144.96'
    # mqtt服务器的端口号
    client.connect(broker, 1883, 60)
    client.username_pw_set('admin', 'admin')
    client.reconnect_delay_set(min_delay=1, max_delay=2000)
    # 启动
    mqttthread = Thread(target=mqttfunction)
    mqttthread.start()

# 启动mqtt
# mqtt_run()

if __name__ == '__main__':
    mqtt_run()