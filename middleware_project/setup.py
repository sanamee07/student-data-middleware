import pika
from middleware.config import RABBITMQ, EXCHANGE_NAME, QUEUE_HIS, QUEUE_PEREGOS, QUEUE_WYSEFLOW, ROUTING_KEY_PEREGOS, ROUTING_KEY_WYSEFLOW

def main():
    # 1. Verbindung zum RabbitMQ-Server aufbauen
    creds  = pika.PlainCredentials(RABBITMQ["user"], RABBITMQ["pass"])
    params = pika.ConnectionParameters(RABBITMQ["host"], RABBITMQ["port"], "/", creds)
    conn   = pika.BlockingConnection(params)
    ch     = conn.channel()

    # 2. Exchange deklarieren (Typ "direct", dauerhaft)
    #    Exchange ist der Vermittler, der Nachrichten anhand eines Routing-Keys an Queues verteilt.
    ch.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="direct",
        durable=True
    )

    # 3. Queues deklarieren (ebenfalls dauerhaft)
    for queue in (QUEUE_HIS, QUEUE_PEREGOS, QUEUE_WYSEFLOW):
        ch.queue_declare(queue=queue, durable=True)

    # 4. Bindings setzen: Sagt RabbitMQ, welche Queue welchen Routing-Key bekommt
    ch.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_PEREGOS,   routing_key=ROUTING_KEY_PEREGOS)
    ch.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_WYSEFLOW,  routing_key=ROUTING_KEY_WYSEFLOW)
    # Bind auch his_queue an den Exchange
    ch.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_HIS, routing_key=QUEUE_HIS)

    print("✅ Queues & Exchange angelegt.")

    conn.close()

if __name__ == "__main__":
    main()
