from middleware.publisher.send_to_queue import publish_message
from middleware.config import ROUTING_KEY_PEREGOS, ROUTING_KEY_WYSEFLOW

def route_student(data: dict):

    #Schickt jeden Studentendatensatz gleichzeitig an Peregos und WyseFlow.
    #Hier können später zusätzliche Filter oder Anpassungen eingefügt werden.
   

    # An Peregos weiterleiten
    publish_message(ROUTING_KEY_PEREGOS, data)

    # An WyseFlow weiterleiten
    publish_message(ROUTING_KEY_WYSEFLOW, data)
