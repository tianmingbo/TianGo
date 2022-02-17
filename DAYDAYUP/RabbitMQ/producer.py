# import pika
#
# queue_name = 'scrape'
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))  # 连接rabbitmq
# channel = connection.channel()  # 频道对象
# channel.queue_declare(queue=queue_name)  # 声明一个队列，队列名叫scrape
# channel.basic_publish(exchange='', routing_key=queue_name, body=b'test')  # routing_key是队列名，body是消息


# 优先级队列
import pika

queue_name = 'scrape1'
max_priority = 100

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))  # 连接rabbitmq
channel = connection.channel()  # 频道对象
# durable 队列持久化
channel.queue_declare(queue=queue_name, arguments={'x-max-priority': max_priority}, durable=True)
while True:
    data, priority = input().split()
    channel.basic_publish(exchange='', routing_key=queue_name,
                          properties=pika.BasicProperties(priority=int(priority), ), body=data)
    print(f'put {data}')
