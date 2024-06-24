import pika

# 连接到队列服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# 创建一个消息队列，并定义回调函数处理收到的消息
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.queue_declare(queue='hello')
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
