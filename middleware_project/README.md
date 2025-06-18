# Middleware Project
Eine RabbitMQ-basierte Middleware zum Verteilen von Studentendaten (HIS → Peregos & WyseFlow)

# Struktur
├── middleware/
│   ├── consumer/
│   │   ├── consumer_base.py
│   │   ├── his_consumer.py
│   │   ├── peregos_consumer.py
│   │   └── wyseflow_consumer.py
│   ├── publisher/
│   │   └── send_to_queue.py
│   ├── router/
│   │   └── route_logic.py
│   ├── utils/
│   │   └── logger.py
│   └── config.py
├── scripts/
│   ├── dummy_peregos.py
│   ├── dummy_wyseflow.py
│   ├── his_cli.py
│   └── run_his.py
├── .env
├── README.md
├── requirements.txt
└── setup.py


## Voraussetzungen

- Python 3.8+  
- RabbitMQ-Server (standard: `http:localhost:5672`)  


## Installation
____________________________________________
1. Installiere die Abhängigkeiten mit:

    windows:    pip install -r requirements.txt
    mac:        sudo install pika
                sudo install python-dotenv
                sudo install flask
                sudo install requests


Lädt alle benötigten Python-Pakete
____________________________________________
2. Exchange und Queues einrichten:

    windows:    python setup.py
    mac:        python3 setup.py

Legt in RabbitMQ die `student_exchange` und die drei Queues (`his_queue`, `peregos_queue`, `wyseflow_queue`) an.
____________________________________________
3. Producer starten (Dummy-Daten):

    windows: python -m scripts.run_his
    mac:     python3 -m scripts.run_his

Simuliert das HIS-System, indem es Beispiel-Studentendaten in die `his_queue` pusht.
_____________________________________________
4. Router-Consumer starten:
    windows: python -m middleware.consumer.his_consumer
    mac:     python3 -m middleware.consumer.his_consumer

Liest Nachrichten aus `his_queue` aus und verteilt sie an die Ziel-Queues `peregos_queue` und `wyseflow_queue`.
____________________________________________
5. Ziel-Consumer starten:

**Peregos-Dummy (Mock-API)**
    windows: python scripts/dummy_peregos.py
    mac:     python3 scripts/dummy_peregos.py

→ Läuft auf `http://localhost:5000` und beantwortet `GET /health` mit 200 sowie `POST /students`.


**WyseFlow-Dummy (Mock-API)**
    windows:    python scripts/dummy_wyseflow.py
    mac:        python3 scripts/dummy_wyseflow.py
→ Läuft auf `http://localhost:5001` und beantwortet `GET /health` mit 200 sowie `POST /thesis`.




**Peregos-Consumer**
    windows: python -m middleware.consumer.peregos_consumer
    mac:     python3 -m middleware.consumer.peregos_consumer
 
 → Wartet auf `GET /health` von Peregos, liest Nachrichten aus `peregos_queue` und sendet per `POST /students` an die Peregos-API.


**WyseFlow-Consumer**
    windows:    python -m middleware.consumer.wyseflow_consumer
    mac:        python3 -m middleware.consumer.wyseflow_consumer
→ Wartet auf `GET /health` von WyseFlow, liest Nachrichten aus `wyseflow_queue` und sendet per `POST /thesis` an die WyseFlow-API.


____________________________________________
Im RabbitMQ-Management (http://localhost:15672/) live ersichtlich, wie Nachrichten durch die Queues fließen.





