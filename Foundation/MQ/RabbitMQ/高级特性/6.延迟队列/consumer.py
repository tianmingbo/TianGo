import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the normal exchange and queue
channel.exchange_declare(exchange='normal_exchange', exchange_type='direct')
channel.queue_declare(queue='normal_queue')
channel.queue_bind(exchange='normal_exchange', queue='normal_queue', routing_key='normal_key')


def callback(ch, method, properties, body):
    print(f"Received: {body.decode('utf-8')}")


channel.basic_consume(queue='normal_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
