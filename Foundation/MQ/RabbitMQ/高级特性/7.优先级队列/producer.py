import pika

# 连接到 RabbitMQ 服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 定义带有优先级的队列
channel.queue_declare(queue='priority_queue', arguments={'x-max-priority': 10})

# 发布具有不同优先级的消息
for i in range(1, 11):
    message = f"Message with priority {i}"
    channel.basic_publish(
        exchange='',
        routing_key='priority_queue',
        body=message,
        properties=pika.BasicProperties(priority=i)
    )
    print(f"[x] Sent '{message}' with priority {i}")

# 关闭连接
connection.close()
