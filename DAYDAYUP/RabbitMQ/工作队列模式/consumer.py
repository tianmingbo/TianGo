import time

import pika

# 建立到 RabbitMQ 的连接
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明任务队列，如果队列不存在，则创建该队列
channel.queue_declare(queue='task_queue', durable=True)


# 处理任务的回调函数
def callback(ch, method, properties, body):
    print("Received %r" % body)
    # 休眠一段时间，模拟任务处理过程
    time.sleep(1)
    # 手动确认消息已经被消费
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 消费消息，并设置同时最多接收的未确认消息数为 1
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

print(' [consumer0] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
