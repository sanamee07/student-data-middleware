from middleware.config              import QUEUE_HIS
from middleware.consumer.consumer_base import start_consumer
from middleware.router.route_logic  import route_student


def handle_his(data: dict):
# Leitet eingehende HIS-Daten an Peregos und WyseFlow weiter
    route_student(data)


if __name__ == "__main__":
    # Startet den Consumer für die HIS-Queue
    start_consumer(QUEUE_HIS, handle_his)
