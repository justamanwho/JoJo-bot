from flask import Flask, request, jsonify
import requests
import os

# Read Setup section in README.md to understand what this is

app = Flask(__name__)
JOJO_BOT_URL = os.getenv('JOJO_BOT_URL', 'http://127.0.0.1:8443/jojo-webhook')

@app.route("/jojo-webhook", methods=["POST"])
def jojo_webhook():
    try:
        update = request.get_json()
        response = requests.post(JOJO_BOT_URL, json=update, timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)