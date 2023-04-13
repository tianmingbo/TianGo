import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the exchange and dead-letter exchange
channel.exchange_declare(exchange='delayed_exchange', exchange_type='direct', arguments={
    'x-delayed-type': 'direct',
    'x-dead-letter-exchange': 'normal_exchange'
})

# Declare the queue with TTL and bind it to the exchange
channel.queue_declare(queue='delay_queue', arguments={'x-message-ttl': 5000})
channel.queue_bind(exchange='delayed_exchange', queue='delay_queue', routing_key='delay_key')

# Publish a message with a delay of 10 seconds
channel.basic_publish(
    exchange='delayed_exchange',
    routing_key='delay_key',
    body='Hello, delayed world!',
    properties=pika.BasicProperties(
        headers={'x-delay': 10000}
    )
)

print("Message sent")
connection.close()
