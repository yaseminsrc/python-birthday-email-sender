import smtplib
import os
import json
from email.message import EmailMessage
from datetime import datetime

# =========================
# CONFIG
# =========================

EMAIL_ADDRESS = os.getenv("BIRTHDAY_EMAIL")
EMAIL_PASSWORD = os.getenv("BIRTHDAY_EMAIL_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

TEST_MODE = False  # True => mail göndermez

BIRTHDAY_FILE = "birthdays.json"
LOG_FILE = "sent_log.txt"

# =========================
# LOAD BIRTHDAYS
# =========================

def load_birthdays():
    with open(BIRTHDAY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# =========================
# LOG SYSTEM
# =========================

def already_sent(email):
    if not os.path.exists(LOG_FILE):
        return False

    today = datetime.now().strftime("%Y-%m-%d")
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f"{email}|{today}" in f.read()

def log_sent(email):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{email}|{today}\n")

# =========================
# EMAIL CONTENT
# =========================

def build_email(name):
    subject = "🎉 Happy Birthday!"
    html = f"""
    <html>
        <body style="font-family:Arial; background:#f4f4f4; padding:20px;">
            <div style="background:white; padding:20px; border-radius:10px;">
                <h2>🎂 Happy Birthday {name}!</h2>
                <p>We wish you happiness, health and success.</p>
                <p style="color:gray;">— Birthday Bot</p>
            </div>
        </body>
    </html>
    """
    return subject, html

# =========================
# SEND EMAIL
# =========================

def send_birthday_email(name, to_email):
    subject, html = build_email(name)

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content("Happy Birthday!")
    msg.add_alternative(html, subtype="html")

    if TEST_MODE:
        print(f"[TEST] Mail gönderilecek → {to_email}")
        return

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# =========================
# MAIN
# =========================

def main():
    today = datetime.now()
    birthdays = load_birthdays()
    sent_any = False

    for person in birthdays:
        if person["month"] == today.month and person["day"] == today.day:
            if already_sent(person["email"]):
                print(f"⚠️ Zaten gönderildi: {person['name']}")
                continue

            send_birthday_email(person["name"], person["email"])
            log_sent(person["email"])
            print(f"🎉 Mail gönderildi: {person['name']}")
            sent_any = True

    if not sent_any:
        print("❌ Bugün doğum günü yok.")

if __name__ == "__main__":
    main()
