from flask import Flask, request, jsonify, render_template
import os, json
from datetime import datetime, timezone

app = Flask(__name__)

DATA_FILE = os.path.join("data", "responses.jsonl")
os.makedirs("data", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/questions")
def questions():
    with open("static/questions.json", encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": data.get("user_id"),
        "answers": data.get("answers")
    }

    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return jsonify({"status": "ok", "message": "Saved"})
