# 🚀 Flask app that serves the live email dashboard
from flask import Flask, render_template, jsonify
import threading
import time
from fetcher import fetch_emails
from database import init_db, store_emails, get_all_emails

app = Flask(__name__)

# 🛠️ Initialize database
init_db()

# 🔁 Background job: fetch new emails every 60 seconds
def auto_fetch():
    while True:
        print("📩 Auto-fetching new emails...")
        emails = fetch_emails()
        store_emails(emails)
        time.sleep(60)

# 🌐 Home route (dashboard UI)
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# 🔌 API endpoint to serve emails as JSON
@app.route("/api/emails")
def api_emails():
    emails = get_all_emails()
    return jsonify(emails)

# 🚀 Background thread for auto-fetching
threading.Thread(target=auto_fetch, daemon=True).start()

# ▶️ Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
