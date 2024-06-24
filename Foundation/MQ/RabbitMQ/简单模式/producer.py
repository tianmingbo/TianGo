import pika

# 连接到队列服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建一个消息队列
channel.queue_declare(queue='hello')

# 发送一条消息
for i in range(100):
    channel.basic_publish(exchange='', routing_key='hello', body=f'Hello World{i}!')
    print(" [x] Sent 'Hello World!'")

# 关闭连接
connection.close()
