import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建一个名为 'my_queue' 的队列
channel.queue_declare(queue='my_queue', arguments={"x-message-ttl": 30000})

# 发布一条带有 TTL 的消息
channel.basic_publish(exchange='', routing_key='my_queue', body='Hello, world!',
                      properties=pika.BasicProperties(expiration='10000'))

connection.close()
