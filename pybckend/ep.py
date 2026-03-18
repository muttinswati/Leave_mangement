#  extracting leave details from mail

import imaplib
import email
from email.header import decode_header
import os
import re
from datetime import datetime

latest_leave_email = None
latest_date = None
latest_reason = ""

# ✅ Extract email address from "From" field
def extract_email(text):
    match = re.search(r'<([^>]+)>', text)
    if match:
        return match.group(1)
    return text.strip()  # fallback: return as-is

# ✅ Extract leave date and reason safely
def extract_leave_details(body):
    global latest_leave_email, latest_date, latest_reason

    # Extract date
    date_match = re.search(r"Date\s*of\s*Leave[:\- ]+\s*(\d{2}-\d{2}-\d{4})", body, re.IGNORECASE)
    leave_date = None
    if date_match:
        date_str = date_match.group(1)
        try:
            leave_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            print("⚠️ Invalid date format found:", date_str)

    # Extract reason
    reason_match = re.search(r"Reason\s*\(.*\)\s*[:\- ]+(.*)", body, re.IGNORECASE)
    reason = reason_match.group(1).strip() if reason_match else ""

    return str(leave_date) if leave_date else None, reason

# Email credentials
user = "staranimex35@gmail.com"
password = os.environ.get("emailpass")

# Connect to Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(user, password)
mail.select("inbox")

# Search for unseen leave request emails
status, messages = mail.search(None,'SUBJECT','"Leave Request"')
for num in messages[0].split():
    status, msg_data = mail.fetch(num, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and part.get_payload(decode=True):
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            latest_leave_email = extract_email(msg["From"])
            print(f"📧 Sender Email: {latest_leave_email}")

            latest_date, latest_reason = extract_leave_details(body)
            print("📅 Leave Date:", latest_date)
            print("📝 Reason:", latest_reason)

            # mail.store(num, '-FLAGS', '\\Seen')
