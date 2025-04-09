# 📥 Email Fetcher using IMAP (Gmail)
from config import EMAIL, PASSWORD
import imaplib
import email
from email.header import decode_header
import re

# 📦 Keyword-based categories for classification
CATEGORIES = {
    "finance": ["invoice", "payment", "salary", "transaction", "bill"],
    "shopping": ["amazon", "flipkart", "order", "shipped", "delivery"],
    "work": ["project", "deadline", "client", "assignment", "update"],
    "meetings": ["meeting", "schedule", "zoom", "teams", "calendar"],
    "notifications": ["notification", "alert", "security", "newsletter"],
    "personal": ["friend", "hi", "hello", "family", "love"],
}

# 🧠 Detect category based on subject and body keywords
def categorize_email(subject, body):
    text = f"{subject} {body}".lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in text:
                return category
    return "other"

# 📨 Main function to fetch all emails from inbox
def fetch_emails():
    # 🔐 Connect to Gmail IMAP server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL, PASSWORD)
    imap.select("inbox")

    # 🔍 Search all email IDs
    status, messages = imap.search(None, "ALL")
    email_ids = messages[0].split()

    emails = []

    # 🔁 Loop through email IDs from latest to oldest
    for eid in reversed(email_ids):  # ✅ reversed = latest first
        _, msg_data = imap.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # 🧠 Decode subject safely
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8", errors="ignore")

        # 📤 From, To, and Date fields
        From = msg.get("From")
        To = msg.get("To")
        Date = msg.get("Date")

        # 📃 Extract plain text body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if (
                    part.get_content_type() == "text/plain"
                    and "attachment" not in str(part.get("Content-Disposition", ""))
                ):
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        # ✅ Detect meeting keywords
        is_meeting = bool(re.search(r'\b(meeting|schedule|zoom|teams|invite|calendar)\b', subject + body, re.I))

        # 🏷️ Detect category
        category = categorize_email(subject, body)

        # 📦 Store parsed email info
        emails.append({
            "sender": From,
            "recipient": To,
            "subject": subject,
            "date": Date,
            "body": body,
            "is_meeting": is_meeting,
            "category": category
        })

    # 🚪 Logout from IMAP server
    imap.logout()

    # 🔄 Reverse to put newest email at top (index 0)
    emails.reverse()  # ✅ This line ensures latest emails come first
    return emails
