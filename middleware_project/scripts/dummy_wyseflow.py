from flask import Flask, request, jsonify

app = Flask(__name__)
message_count = 0


@app.route("/health", methods=["GET"])
def health():
    # Einfacher Health-Check: liefert HTTP 200 und ein kurzes JSON zurück
    return jsonify({"status": "ok"}), 200

@app.route("/thesis", methods=["POST"])
def thesis():
    global message_count

    data = request.json
    message_count += 1
    current = message_count

    print("🔔 Received WyseFlow payload:")
    print(data)
    print(f"🔢 Insgesamt angekommen (WyseFlow): {current}\n")

    return "", 200

if __name__ == "__main__":
    # Starte den Flask-Server auf http://localhost:5001
    app.run(port=5001)



