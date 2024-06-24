import pika

# 建立到 RabbitMQ 的连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 申明 exchange，设置 exchange 类型为 topic
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# 发送消息
for i in range(100):
    message = 'Hello World!'
    routing_key = 'com.example.app.events.info'
    channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)

# 关闭连接
connection.close()
