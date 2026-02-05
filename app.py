from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Allows all origins; can restrict to your domain later

ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY")
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")  # optional if needed

@app.route("/first-push", methods=["POST"])
def first_push():
    data = request.get_json()
    player_id = data.get("playerId")

    if not player_id:
        return jsonify({"error": "No playerId provided"}), 400

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {ONESIGNAL_API_KEY}"
    }

    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "include_player_ids": [player_id],
        "headings": {"en": "Your Invoice is Ready!"},
        "contents": {"en": "Click here to view your invoice."}
    }

    response = requests.post("https://onesignal.com/api/v1/notifications", json=payload, headers=headers)
    print("OneSignal response:", response.text)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets the PORT environment variable
    app.run(host="0.0.0.0", port=port)

