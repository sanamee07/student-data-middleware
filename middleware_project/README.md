# Middleware Project  
A RabbitMQ-based middleware for distributing student data (HIS → Peregos & WyseFlow)

# Structure
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

## Requirements

- Python 3.8+  
- RabbitMQ server (default: `http://localhost:5672`)  

---

## Installation

____________________________________________  
1. Install dependencies:
```
    windows:        pip install -r requirements.txt
   
    mac:            sudo install pika,python-dotenv,flask,requests
```

Installs all required Python packages.
____________________________________________
2. Set up the exchange and queues:

```
    windows:    python setup.py
   
    mac:        python3 setup.py
```

This creates the student_exchange and the three queues:
his_queue, peregos_queue, and wyseflow_queue in RabbitMQ.
____________________________________________
3. Start the producer (dummy data):

```
    windows: python -m scripts.run_his
   
    mac:     python3 -m scripts.run_his
```

Simulates the HIS system by pushing sample student data into the his_queue.
_____________________________________________
4. Start the router consumer:

```
    windows: python -m middleware.consumer.his_consumer
   
    mac:     python3 -m middleware.consumer.his_consumer
```

Reads messages from his_queue and forwards them to the target queues peregos_queue and wyseflow_queue.
____________________________________________
5. Start the target consumers:


**Peregos-Dummy (Mock-API)**
```
    windows: python scripts/dummy_peregos.py
    
    mac:     python3 scripts/dummy_peregos.py
```
→ Runs on http://localhost:5000, responds with 200 to GET /health, and accepts POST /students.


**WyseFlow-Dummy (Mock-API)**
```
    windows:    python scripts/dummy_wyseflow.py
    
    mac:        python3 scripts/dummy_wyseflow.py
```
→ Runs on http://localhost:5001, responds with 200 to GET /health, and accepts POST /thesis.




**Peregos-Consumer**
   ``` 
    windows: python -m middleware.consumer.peregos_consumer
    
    mac:     python3 -m middleware.consumer.peregos_consumer
 ```
→ Waits for GET /health from Peregos, reads from peregos_queue, and sends data to POST /students.


**WyseFlow-Consumer**
```    
    windows:    python -m middleware.consumer.wyseflow_consumer
    
    mac:        python3 -m middleware.consumer.wyseflow_consumer
```
→ Waits for GET /health from WyseFlow, reads from wyseflow_queue, and sends data to POST /thesis.



____________________________________________
You can monitor the live message flow in the RabbitMQ Management UI:
➡️ http://localhost:15672/





