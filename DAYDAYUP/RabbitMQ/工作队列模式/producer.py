import pika

# 建立到 RabbitMQ 的连接
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明任务队列，如果队列不存在，则创建该队列
channel.queue_declare(queue='task_queue', durable=True)

# 发送任务消息到任务队列
for i in range(100):
    message = f'Hello, World-{i}!'
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # 消息持久化
                          ))

    print(" [x] Sent %r" % message)

# 关闭连接
connection.close()
