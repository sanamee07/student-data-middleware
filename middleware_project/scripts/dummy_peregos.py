from flask import Flask, request, jsonify

app = Flask(__name__)
message_count = 0


@app.route("/health", methods=["GET"])
def health():
    # Einfacher Health-Check: liefert HTTP 200 und ein kurzes JSON zurück
    return jsonify({"status": "ok"}), 200

@app.route("/students", methods=["POST"])
def students():
    global message_count

    data = request.json
    message_count += 1
    current = message_count

    print("🔔 Received student payload:")
    print(data)
    print(f"🔢 Insgesamt angekommen (Peregos): {current}\n")

    return "", 200

if __name__ == "__main__":
    # Starte den Flask-Server auf http://localhost:5000
    app.run(port=5000)
