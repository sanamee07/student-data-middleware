import json
import pika
from middleware.config import RABBITMQ, EXCHANGE_NAME
from middleware.utils.logger import logger

def publish_message(routing_key: str, message: dict):
    #Baut eine Verbindung zu RabbitMQ auf und schickt einen JSON-Payload 
    # mit dem angegebenen Routing-Key an die Exchange.
    
    creds = pika.PlainCredentials(RABBITMQ["user"], RABBITMQ["pass"])
    params = pika.ConnectionParameters(
        host=RABBITMQ["host"],
        port=RABBITMQ["port"],
        credentials=creds
    )
    connection = pika.BlockingConnection(params)
    channel    = connection.channel()

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # persistent
    )
    logger.info(f"▶️ Gesendet [{routing_key}]: {message}")
    connection.close()
