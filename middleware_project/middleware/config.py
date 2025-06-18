from os import environ
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env (z.B. RABBITMQ_HOST, RABBITMQ_PORT, QUEUE_NAMES, API_URLS)
load_dotenv()  

# RabbitMQ‐Verbindungsparameter
# Hier werden Host, Port, Username und Passwort aus den Umgebungsvariablen gelesen.
RABBITMQ = {
    "host":   environ.get("RABBITMQ_HOST"),
    "port":   int(environ.get("RABBITMQ_PORT", 5672)),
    "user":   environ.get("RABBITMQ_USER"),
    "pass":   environ.get("RABBITMQ_PASS"),
}

# Exchange und Queues
# - EXCHANGE_NAME: Gemeinsame Exchange, über die alle eingehenden HIS-Daten verteilt werden.
# - QUEUE_HIS, QUEUE_PEREGOS, QUEUE_WYSEFLOW: Die einzelnen Queues, in denen Nachrichten
#   aufbewahrt werden, bis ein Consumer sie abholt.
EXCHANGE_NAME       = environ.get("EXCHANGE_NAME")
QUEUE_HIS           = environ.get("QUEUE_HIS")
QUEUE_PEREGOS       = environ.get("QUEUE_PEREGOS")
QUEUE_WYSEFLOW      = environ.get("QUEUE_WYSEFLOW")

# Routing-Keys für das Publishing
ROUTING_KEY_PEREGOS   = environ.get("ROUTING_KEY_PEREGOS")
ROUTING_KEY_WYSEFLOW  = environ.get("ROUTING_KEY_WYSEFLOW")
