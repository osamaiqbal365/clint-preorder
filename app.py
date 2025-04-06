from flask import Flask, request, jsonify, render_template
import os
from azure.storage.queue import QueueClient

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    try:
        queue_url = os.environ.get("AZURE_QUEUE_URL")
        queue_client = QueueClient.from_queue_url(queue_url)
        queue_client.send_message(str(data))
        return jsonify({"status": "queued"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
