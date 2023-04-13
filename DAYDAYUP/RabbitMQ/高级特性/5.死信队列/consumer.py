import pika

# 创建连接和频道对象
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建普通队列
channel.queue_declare(queue='normal_queue', arguments={
    'x-dead-letter-exchange': 'dlx_exchange',
    'x-dead-letter-routing-key': 'dlx_routing_key'
})

# 创建 DLX 交换器
channel.exchange_declare(exchange='dlx_exchange', exchange_type='direct')

# 创建 DLQ 队列
channel.queue_declare(queue='dlq_queue')

# 绑定 DLX 交换器和 DLQ 队列
channel.queue_bind(queue='dlq_queue', exchange='dlx_exchange', routing_key='dlx_routing_key')


def callback(ch, method, properties, body):
    # 模拟消息处理失败，抛出异常
    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


# 监听普通队列，并设置消息处理回调函数
channel.basic_qos(prefetch_count=100)  # 限流
channel.basic_consume(queue='normal_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
