# 🗄️ Email Storage in SQLite
import sqlite3

DB_FILE = "emails.db"

# 🛠️ Create table if not exists
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            recipient TEXT,
            subject TEXT,
            date TEXT,
            body TEXT,
            is_meeting INTEGER,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 💾 Store unique emails
def store_emails(emails):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    for email in emails:
        cur.execute("SELECT * FROM emails WHERE sender=? AND subject=? AND date=?", 
                    (email['sender'], email['subject'], email['date']))
        exists = cur.fetchone()
        if not exists:
            cur.execute('''
                INSERT INTO emails (sender, recipient, subject, date, body, is_meeting, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (email['sender'], email['recipient'], email['subject'], 
                  email['date'], email['body'], int(email['is_meeting']), email['category']))
    conn.commit()
    conn.close()

# 📤 Read all emails in latest-first order
def get_all_emails():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT sender, recipient, subject, date, body, is_meeting, category FROM emails ORDER BY id DESC")
    emails = cur.fetchall()
    conn.close()

    # Format as list of dicts
    result = []
    for e in emails:
        result.append({
            "sender": e[0],
            "recipient": e[1],
            "subject": e[2],
            "date": e[3],
            "body": e[4],
            "is_meeting": bool(e[5]),
            "category": e[6]
        })
    return result
