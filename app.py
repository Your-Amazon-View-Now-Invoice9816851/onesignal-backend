from flask import Flask, request, jsonify
import requests
import time
import os

app = Flask(__name__)

ONESIGNAL_APP_ID = "59378825-1e42-4024-a9f1-87553ae750f8"
ONESIGNAL_API_KEY = os.environ.get("ONESIGNAL_API_KEY")

sent_users = set()

@app.route("/first-push", methods=["POST"])
def first_push():
    data = request.get_json()
    player_id = data.get("playerId")

    if not player_id or player_id in sent_users:
        return jsonify({"status": "ignored"})

    sent_users.add(player_id)

    time.sleep(5)

    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "include_player_ids": [player_id],
        "headings": {"en": "Invoice Ready"},
        "contents": {
            "en": "Your invoice is now available. You may review it at your convenience."
        }
    }

    headers = {
        "Authorization": f"Basic {ONESIGNAL_API_KEY}",
        "Content-Type": "application/json"
    }

    requests.post(
        "https://onesignal.com/api/v1/notifications",
        json=payload,
        headers=headers,
        timeout=10
    )

    return jsonify({"status": "sent"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
