import pika

# 创建连接和频道对象
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建普通队列
channel.queue_declare(queue='normal_queue', arguments={
    'x-dead-letter-exchange': 'dlx_exchange',
    'x-dead-letter-routing-key': 'dlx_routing_key'
})
for i in range(100):
    channel.basic_publish(exchange='', routing_key='normal_queue', body=f'Hello World{i}!',
                          )
    print(" [x] Sent 'Hello World!'")
# 关闭连接
connection.close()
