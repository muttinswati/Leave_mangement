#  booking confirmation from teachers
import imaplib
import email
import os
import re
from datetime import datetime

def booking_confirmations():
    user = "staranimex35@gmail.com"
    password = os.environ.get("emailpass")

    print("📌 Email Password Loaded:", "Yes" if password else "No")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user, password)
    print("✅ Logged in to Gmail")

    mail.select("inbox")

    # Filter: All emails (both seen and unseen) from today onwards
    today = datetime.today().strftime("%d-%b-%Y")  # e.g., "06-May-2025"
    status, messages = mail.search(None, f'(SENTSINCE {today})')
    email_ids = messages[0].split()
    print(f"📨 Total emails since {today}: {len(email_ids)}")

    extracted_list = []

    for i, num in enumerate(email_ids):
        print(f"📧 Checking email #{num.decode()}")
        status, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                body = ""

                # Extract body
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type in ["text/plain", "text/html"]:
                            charset = part.get_content_charset() or "utf-8"
                            try:
                                body = part.get_payload(decode=True).decode(charset, errors="ignore")
                                break
                            except Exception as e:
                                print(f"❌ Error decoding part: {e}")
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                body = re.sub(r'<[^>]*>', '', body)  # Remove HTML
                body = body.strip()

                # Extract sender
                from_header = msg.get("From")
                email_match = re.search(r'<([^>]+)>', from_header)
                sender_email = email_match.group(1) if email_match else from_header.strip()

                # Extract unique code (handle both "Your unique code" and "your valid unique code")
                code_match = re.search(r"(?:your valid unique code|Your unique code):\s*(\S+)", body, re.IGNORECASE)
                unique_code = code_match.group(1) if code_match else None

                # Extract FID
                fid = unique_code.split("#")[0] if unique_code else None

                if sender_email and unique_code and fid:
                    extracted_list.append((sender_email, unique_code, fid))
                    print(f"✅ Match Found:\n  From: {sender_email}\n  Unique Code: {unique_code}\n  FID: {fid}")
                else:
                    print("⚠️ Email skipped: missing sender/code/fid")

    return extracted_list

# Call for test
if __name__ == "__main__":
    booking_confirmations()
