import pika

# 建立到 RabbitMQ 的连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 申明 exchange，设置 exchange 类型为 direct，同时创建一个随机名称的不持久化、独占的队列
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
result = channel.queue_declare(queue='', durable=False, exclusive=True)
queue_name = result.method.queue

# 将队列绑定到交换机上，指定需要接收的路由键为 "info" 和 "warning"
channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key='info')
channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key='warning')
channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key='error')


# 处理消息的回调函数
def callback(ch, method, properties, body):
    print("Received %r" % body)


# 开始消费消息
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages in queue %s. To exit press CTRL+C' % queue_name)
channel.start_consuming()

# 关闭连接
connection.close()
