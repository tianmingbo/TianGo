import random

import pika

# 建立到 RabbitMQ 的连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 申明 exchange，设置 exchange 类型为 direct
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# 发送消息
for i in range(100):
    message = f'Hello World-{i}!'
    routing_key = random.choice(['info', 'error', 'warning'])
    channel.basic_publish(exchange='direct_logs', routing_key=routing_key, body=message)

# 关闭连接
connection.close()
