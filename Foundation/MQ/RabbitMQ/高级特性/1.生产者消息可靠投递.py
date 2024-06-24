"""
 confirm 确认模式
 return 退回模式
"""

# confirm
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 设置确认模式为消息确认模式
channel.confirm_delivery()

# 当将 mandatory 参数设置为 True 时，如果消息无法路由到指定的队列，则会将消息返回给生产者，并调用生产者的 on_return_callback 回调函数
try:
    for i in range(10):
        message = f"Hello World {i}"
        channel.basic_publish(exchange='', routing_key='hello', body=message, mandatory=True)
except pika.exceptions.UnroutableError:
    print('Message could not be confirmed')

connection.close()
