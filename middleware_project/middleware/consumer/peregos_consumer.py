import time
import requests
from middleware.config                 import QUEUE_PEREGOS
from middleware.consumer.consumer_base import start_consumer
from middleware.utils.logger           import logger

def is_peregos_up():
    try:
        # Prüft per GET /health, ob der Peregos-Server erreichbar ist (Status 200).
        resp = requests.get("http://localhost:5000/health", timeout=2)
        return resp.status_code == 200
    except:
        return False

def handle_peregos(data: dict):
    #Behandelt einen einzelnen Datensatz:
    #1) Health-Check: Falls Peregos gerade nicht erreichbar, Exception → requeue
    #2) POST /students: Bei Verbindungsfehler oder HTTP ≠ 200 Exception → requeue
    #3) Nur bei 200 OK: Erfolgs-Log, Consumer ackt die Nachricht



    # 1) Per-Message Health-Check
    if not is_peregos_up():
        logger.warning("⚠️ Peregos vorübergehend offline – lege Nachricht zurück in die Queue, warte 5 Sekunden …")
        time.sleep(5)
        # Exception werfen, damit consumer_base requeue=True ausführt
        raise RuntimeError("Peregos offline – Nachricht wird später erneut versucht")

    # 2) POST an /students ausführen
    url = "http://localhost:5000/students"  
    try:
        resp = requests.post(url, json=data, timeout=5)
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Verbindung zu Peregos fehlgeschlagen: {e} – warte 5 Sekunden, requeue")
        time.sleep(5)
        raise RuntimeError("POST-Abbruch wegen Verbindungsproblem – requeue")

    if resp.status_code != 200:
        logger.error(f"❌ Peregos-Error: HTTP {resp.status_code} – warte 5 Sekunden, requeue")
        time.sleep(5)
        raise RuntimeError(f"Peregos HTTP-Error {resp.status_code} – requeue")

    # 3) Erfolgreich verarbeitet
    logger.info(f"✅ Peregos OK: {data.get('id', '<kein ID>')}")

if __name__ == "__main__":
     # Startup-Health-Check: Warten auf /health=200, bevor der Consumer Nachrichten abholt
    while not is_peregos_up():
        logger.warning("⚠️ Peregos-Server offline beim Start – warte 10 Sekunden …")
        time.sleep(10)

    logger.info("✅ Peregos ist jetzt erreichbar → Starte den Peregos-Consumer")
    start_consumer(QUEUE_PEREGOS, handle_peregos)
