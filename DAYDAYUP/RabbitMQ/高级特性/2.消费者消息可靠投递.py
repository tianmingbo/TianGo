import pika


# 定义回调函数处理每条消息
def callback(ch, method, properties, body):
    print("Received message:", body.decode())
    # 消息处理完成后发送确认
    ch.basic_ack(delivery_tag=method.delivery_tag)


# def callback(ch, method, properties, body):
#     print("Received message:", body.decode())
#     """
#     delivery_tag：表示消息的唯一标识符，即与 basic_ack() 方法中相同的参数。
# multiple：一个布尔值，它指定了是否拒绝已经被 RabbitMQ 分配的所有未确认的消息。如果设置为 True，则表示将 delivery_tag 之前的所有未确认的消息都拒绝掉；如果设置为 False，则只拒绝当前这条消息。
# requeue：一个布尔值，它指定了是否将被拒绝的消息重新排队等待处理。如果设置为 True，则被拒绝的消息将返回到队列中，等待下一次被消费；如果设置为 False，则被拒绝的消息将会被删除。
#     """
#     ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


# 创建连接和通道
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 设置应答模式为手动确认
channel.basic_qos(prefetch_count=1)  # 限流
channel.basic_consume(queue='hello', on_message_callback=callback)

# 开始消费消息
channel.start_consuming()
