# import pika
#
# queue_name = 'scrape'
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # 连接rabbitmq
# channel = connection.channel()  # 频道对象
# channel.queue_declare(queue=queue_name)
#
#
# def callback(ch, method, properties, body):
#     print(f'get {body}')
#
#
# # auto_ack 消费者自动通知消息队列当前消息已处理
# channel.basic_consume(queue='scrape', auto_ack=True, on_message_callback=callback)
# channel.start_consuming()


# 优先级队列
import pika

queue_name = 'scrape1'
max_priority = 100

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # 连接rabbitmq
channel = connection.channel()  # 频道对象

while True:
    input()
    method_frame, header, body = channel.basic_get(queue=queue_name, auto_ack=True)
    if body:
        print(method_frame, header, body)
