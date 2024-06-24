import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 创建一个名为 "task_queue" 的队列，并声明一个持久化队列，durable
channel.queue_declare(queue='task_queue', durable=True)

# 消息持久化：delivery_mode=2
message = 'Hello world!'
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2))
print(" [x] Sent %r" % message)
connection.close()
