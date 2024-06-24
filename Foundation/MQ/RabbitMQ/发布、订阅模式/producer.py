"""
直接交换机（Direct Exchange）：根据消息的 Routing Key 与绑定队列的 Routing Key 完全匹配来确定路由规则。

主题交换机（Topic Exchange）：根据消息的 Routing Key 和绑定队列的 Routing Key 使用通配符匹配规则来确定路由规则。例如，可以使用 * 匹配一个单词，使用 # 匹配多个单词或者零个单词。

扇形交换机（Fanout Exchange）：将收到的消息广播给所有与之绑定的队列，不需要 Routing Key。

头部交换机（Headers Exchange）：根据消息中指定的 Header 属性与队列绑定的 Header 参数进行匹配来确定路由规则。
"""
import pika

# 建立到 RabbitMQ 的连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明 fanout 类型的交换机
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# 发送消息到交换机
for i in range(100):
    message = f'Hello, World-{i}!'
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message)

    print(" [x] Sent %r" % message)

# 关闭连接
connection.close()
