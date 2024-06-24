import pika


# 定义回调函数处理每条消息
def callback(ch, method, properties, body):
    print("Received message:", body.decode())
    # 消息处理完成后发送确认
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 设置应答模式为手动确认
channel.basic_qos(prefetch_count=2)  # 限流
channel.basic_consume(queue='hello', on_message_callback=callback)

# 开始消费消息
channel.start_consuming()
