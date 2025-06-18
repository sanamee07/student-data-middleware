import json
import pika
from ..config import RABBITMQ
from ..utils.logger import logger

def start_consumer(queue_name: str, handler):




    # Verbindungskonfiguration zusammenbauen
    creds  = pika.PlainCredentials(
        RABBITMQ["user"],
        RABBITMQ["pass"]
        )
    params = pika.ConnectionParameters(
        host=RABBITMQ["host"],
        port=RABBITMQ["port"],
        credentials=creds
    )
    # Verbindung aufbauen
    connection = pika.BlockingConnection(params)
    channel    = connection.channel()

    # Nur eine Nachricht gleichzeitig, bis ack/nack zurückkommt
    channel.basic_qos(prefetch_count=1)

    # Callback für eingehende Nachrichten registrieren
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=lambda ch, method, props, body: _wrapper(ch, method, body, handler),
        auto_ack=False
    )
    logger.info(f"🔌 Consumer gestartet: {queue_name}")
    channel.start_consuming()

# Liest den JSON-Text, ruft handler mit den Daten auf. Wenn alles klappt, wird die Nachricht bestätigt, sonst zurück in die Queue gelegt.
def _wrapper(ch, method, body, handler):
    data = json.loads(body)
    try:
        handler(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"✅ {method.routing_key} verarbeitet: {data}")
    except Exception as e:
        logger.error(f"❌ Fehler bei {method.routing_key}: {e} → Nachricht wird erneut in Queue gelegt")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
