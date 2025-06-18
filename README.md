# 🎓 Student Data Middleware (HIS → Peregos & WyseFlow)

This project implements a lightweight middleware to automatically route student data from the **HIS** system to **Peregos** and **WyseFlow** using **RabbitMQ**.  
It was developed as part of the course *Architecture and Integration* at Frankfurt University of Applied Sciences.

---
## 📌 Overview

Manual entry of student data into Peregos and WyseFlow is error-prone and time-consuming. This middleware solves the problem by introducing an asynchronous, decoupled architecture that:
- **receives** data from HIS,
- **routes** it through a central exchange,
- and **delivers** it to Peregos and WyseFlow using dedicated queues and REST APIs.

## 🧭 Architecture

The architecture is message-based and uses RabbitMQ for decoupled communication between systems:
![image](https://github.com/user-attachments/assets/cc6a8607-6d8f-42d8-abba-fae8b6d05ed1)
1. **HIS** publishes data to the `student_exchange`.
2. A message with routing key `studentdata.his` is queued in `his_queue`.
3. A consumer reads the message and republishes it to two queues:
   - `peregos_queue` (→ Peregos)
   - `wyseflow_queue` (→ WyseFlow)

---

## ⚙️ Technologies Used
- Python 3.8+
- RabbitMQ (message broker)
- Flask (dummy servers for Peregos/WyseFlow)
- pika (Python RabbitMQ client)
- dotenv (environment configuration)


## 🚀 How to Use

> The full setup instructions and usage steps can be found in the **existing project-level README.md** inside the repository.


📎 License
This project is part of a university prototype and is intended for educational use.
