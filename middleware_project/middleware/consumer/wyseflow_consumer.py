import time
import requests
from middleware.config                 import QUEUE_WYSEFLOW
from middleware.consumer.consumer_base import start_consumer
from middleware.utils.logger           import logger

def is_wyseflow_up():
    try:
        #Prüft per GET /health, ob der WyseFlow-Server erreichbar ist (Status 200).
        resp = requests.get("http://localhost:5001/health", timeout=2)
        return resp.status_code == 200
    except:
        return False

def handle_wyseflow(data: dict):
    #Behandelt einen einzelnen Datensatz:
    #1) Health-Check: Falls WyseFlow gerade nicht erreichbar, Exception → requeue
    #2) POST /thesis: Bei Verbindungsfehler oder HTTP ≠ 200 Exception → requeue
    #3) Nur bei 200 OK: Erfolgs-Log, Consumer ackt die Nachricht


    # 1) Per-Message Health-Check
    if not is_wyseflow_up():
        logger.warning("⚠️ WyseFlow vorübergehend offline – lege Nachricht zurück in die Queue, warte 5 Sekunden …")
        time.sleep(5)
        # Exception werfen, damit consumer_base requeue=True ausführt
        raise RuntimeError("WyseFlow offline – Nachricht wird später erneut versucht")

    # 2) POST an /thesis 
    url = "http://localhost:5001/thesis" 
    try:
        resp = requests.post(url, json=data, timeout=5)
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Verbindung zu WyseFlow fehlgeschlagen: {e} – warte 5 Sekunden, requeue")
        time.sleep(5)
        raise RuntimeError("POST-Abbruch wegen Verbindungsproblem – requeue")

    if resp.status_code != 200:
        logger.error(f"❌ WyseFlow-Error: HTTP {resp.status_code} – warte 5 Sekunden, requeue")
        time.sleep(5)
        raise RuntimeError(f"WyseFlow HTTP-Error {resp.status_code} – requeue")

    # 3) Erfolgreich verarbeitet
    logger.info(f"✅ WyseFlow OK: {data.get('id', '<kein ID>')}")

if __name__ == "__main__":
    # Einmaliger Startup-Health-Check
    while not is_wyseflow_up():
        logger.warning("⚠️ WyseFlow-Server offline beim Start – warte 10 Sekunden …")
        time.sleep(10)

    logger.info("✅ WyseFlow ist jetzt erreichbar → Starte den WyseFlow-Consumer")
    start_consumer(QUEUE_WYSEFLOW, handle_wyseflow)
