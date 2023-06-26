import pika

# 连接到 RabbitMQ 服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 定义带有优先级的队列
channel.queue_declare(queue='priority_queue', arguments={'x-max-priority': 10})


# 回调函数
def callback(ch, method, properties, body):
    print('[x] Received:', body.decode('utf-8'))


# QoS配置，确保按照优先级从高到低进行处理
channel.basic_qos(prefetch_count=1)

# 消费消息
channel.basic_consume(queue='priority_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
