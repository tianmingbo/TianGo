# -*- coding：utf8 -*-
# @Project : flask_review
# @Author : qxq
# @Time : 2020/2/15 5:17 PM

import datetime
import json
import sys
import paho.mqtt.client as mqtt
import time


class EMQClient(object):
    """
    rc  0：连接成功
        1：连接被拒绝-协议版本不正确
        2：连接被拒绝-无效的客户端标识符
        3：连接被拒绝-服务器不可用
        4：连接被拒绝-用户名或密码错误
        5：连接被拒绝-未经授权6-255：当前未使用。
    """

    def __init__(self, host, port=1883, keepalive=60, cliend_id=None, user=None, pwd=None, qos=0):
        self.qos = qos
        if cliend_id:
            self.emq_client = mqtt.Client(client_id=cliend_id)
        else:
            self.emq_client = mqtt.Client()
        self.emq_client.on_connect = self.on_connect
        self.emq_client.on_disconnect = self.on_disconnect
        # self.emq_client.on_subscribe = self.on_subscribe

        # 接收消息
        self.emq_client.on_message = self.on_message
        # 设置用户密码，如果没有设置用户，这里可以省略
        self.emq_client.username_pw_set(user, pwd)
        self.emq_client.connect(host, port, keepalive=keepalive)
        self.emq_client.loop_start()

    def get_time(self):
        # 获取时间

        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    def on_connect(self, client, userdata, flags, rc):
        # 连接时 callback

        print(self.get_time(), "[consumer]Connected with result code " + str(rc))
        if rc == 0:
            print('connected to mqtt with resurt code ', rc, self.qos)
            # 订阅主题
            sub_result = client.subscribe('vehicleInfoTopic', qos=self.qos)
            print(self.get_time(), "Connected with result is status: {}, mid: {})".format(*sub_result))
        else:
            print(self.get_time(), " connect failed")

    def on_disconnect(self, client, userdata, rc):
        # 在连接断开时的 callback

        print("Disconnection returned result:" + str(rc))
        self.emq_client.disconnect()

    def on_subscribe(self, client, userdata, mid, granted_qos):
        # 开始时订阅 callback

        print(self.get_time(), "Begin subscribe topic with ", mid)

    def on_message(self, client, userdata, message):
        # 接收消息 callback
        print(message.timestamp)
        print(datetime.datetime.now().timestamp())
        print(time.time())
        print(message.payload)
        payload = message.payload.decode('utf-8')
        payload_dict = json.loads(message.payload.decode('utf-8'))
        print(type(payload_dict), payload_dict)
        print(self.get_time(),
              "Received message: {} type: {} on topic: {} with QoS: {}".format(payload, type(payload), message.topic,
                                                                               message.qos))
        print('=' * 30)

    def to_subscribe(self, task_topic):
        # 订阅主题

        print(self.get_time(), "新增订阅主题：{}".format(task_topic))
        rc, mid = self.emq_client.subscribe(task_topic, qos=self.qos)
        print('subscribe ret', rc, mid)
        if rc == 0:
            print(self.get_time(), "success sub topic:{} with mid:{}".format(task_topic, mid))
        else:
            print(self.get_time(), "failed to sub topic:{} rc:{}".format(task_topic, rc))

    def to_publish(self, task_topic, message):
        # 发布

        try:
            # time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            time_now = time.time()
            payload = {"msg": message, "date": time_now}
            # publish(主题：Topic; 消息内容)
            rc, mid = self.emq_client.publish(task_topic, json.dumps(payload, ensure_ascii=False))
            print('publish ret', rc, mid)
            if rc == 0:
                print(self.get_time(), " success pub message with id: ", mid)
            else:
                print(self.get_time(), "failed to pub message rc", rc)
        except ValueError as err_str:
            print(self.get_time(), "please check your parameters: ", err_str)
        except Exception as e:
            print(e)

    def run(self):
        # 以start方式运行，需要启动一个守护线程，让服务端运行，否则会随主线程死亡
        self.emq_client.loop_start()
        # 以forever方式阻塞运行
        # self.emq_client.loop_forever()

    def server_stop(self):
        # 停止

        self.emq_client.loop_stop()
        sys.exit(0)


if __name__ == "__main__":
    cliend_id = "qwertertrt"
    host = '192.168.210.31'
    port = 1883
    keepalive = 60
    emq_client = EMQClient(host, port, keepalive, cliend_id=cliend_id, user='admin', pwd='123456', qos=0)
    while True:
        flag = input("请输入：(1:run, 2:stop, 3:订阅主题, 4:退订主题, 5:发布主题消息)")
        if flag == "1":
            emq_client.run()
        elif flag == "2":
            emq_client.server_stop()
        elif flag == "3":
            task_topic = input("请输入订阅主题：")
            emq_client.to_subscribe(task_topic)
        elif flag == "4":
            task_topic = input("请输入退订主题：")
            emq_client.emq_client.unsubscribe(task_topic)
        elif flag == "5":
            task_topic = input("请输入主题：")
            message = input("请输入消息内容：")
            emq_client.to_publish(task_topic, message)
        else:
            print('输入有误～')