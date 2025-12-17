import smtplib
import os
import json
import logging
import argparse
from email.message import EmailMessage
from datetime import datetime

# =========================
# LOGGING CONFIG
# =========================

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# CONFIG
# =========================

class Config:
    EMAIL_ADDRESS = os.getenv("BIRTHDAY_EMAIL")
    EMAIL_PASSWORD = os.getenv("BIRTHDAY_EMAIL_PASSWORD")

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 465

    BIRTHDAY_FILE = "birthdays.json"
    SENT_LOG_FILE = "sent_log.txt"

    TEST_MODE = False
    DRY_RUN = False
    FORCE_DATE = None


# =========================
# EMAIL SERVICE
# =========================

class EmailService:
    def __init__(self, config: Config):
        self.config = config

    def send(self, to_email: str, subject: str, html: str):
        if self.config.DRY_RUN:
            logging.info(f"[DRY-RUN] Email skipped for {to_email}")
            print(f"[DRY-RUN] Mail → {to_email}")
            return

        msg = EmailMessage()
        msg["From"] = self.config.EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content("Happy Birthday!")
        msg.add_alternative(html, subtype="html")

        if self.config.TEST_MODE:
            logging.info(f"[TEST MODE] Email prepared for {to_email}")
            print(f"[TEST] Mail gönderilecek → {to_email}")
            return

        try:
            with smtplib.SMTP_SSL(
                self.config.SMTP_SERVER,
                self.config.SMTP_PORT
            ) as server:
                server.login(
                    self.config.EMAIL_ADDRESS,
                    self.config.EMAIL_PASSWORD
                )
                server.send_message(msg)

            logging.info(f"Email sent to {to_email}")

        except Exception as e:
            logging.error(f"Email sending failed: {e}")
            raise


# =========================
# BIRTHDAY SERVICE
# =========================

class BirthdayService:
    def __init__(self, config: Config, email_service: EmailService):
        self.config = config
        self.email_service = email_service

    def load_birthdays(self):
        with open(self.config.BIRTHDAY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def already_sent(self, email: str) -> bool:
        if not os.path.exists(self.config.SENT_LOG_FILE):
            return False

        today = self.get_today().strftime("%Y-%m-%d")
        with open(self.config.SENT_LOG_FILE, "r", encoding="utf-8") as f:
            return f"{email}|{today}" in f.read()

    def log_sent(self, email: str):
        today = self.get_today().strftime("%Y-%m-%d")
        with open(self.config.SENT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{email}|{today}\n")

    def build_email(self, name: str):
        subject = "🎉 Happy Birthday!"
        html = f"""
        <html>
            <body style="font-family:Arial; background:#f4f4f4; padding:20px;">
                <div style="background:white; padding:20px; border-radius:10px;">
                    <h2>🎂 Happy Birthday {name}!</h2>
                    <p>We wish you happiness and success.</p>
                    <p style="color:gray;">— Birthday Bot</p>
                </div>
            </body>
        </html>
        """
        return subject, html

    def get_today(self):
        if self.config.FORCE_DATE:
            month, day = map(int, self.config.FORCE_DATE.split("-"))
            return datetime(datetime.now().year, month, day)
        return datetime.now()

    def run(self):
        logging.info("BirthdayService started")

        birthdays = self.load_birthdays()
        today = self.get_today()
        sent_any = False

        for person in birthdays:
            if person["month"] == today.month and person["day"] == today.day:
                if self.already_sent(person["email"]):
                    print(f"⚠️ It's already been sent: {person['name']}")
                    continue

                subject, html = self.build_email(person["name"])
                self.email_service.send(
                    person["email"],
                    subject,
                    html
                )

                if not self.config.DRY_RUN and not self.config.TEST_MODE:
                    self.log_sent(person["email"])

                print(f"🎉 Processed: {person['name']}")
                sent_any = True

        if not sent_any:
            print("❌ There is no birthday today.")

        logging.info("BirthdayService finished")


# =========================
# CLI
# =========================

def parse_args():
    parser = argparse.ArgumentParser(
        description="🎉 Automated Birthday Email Sender"
    )
    parser.add_argument("--test", action="store_true", help="Test mode")
    parser.add_argument("--dry-run", action="store_true", help="No emails sent")
    parser.add_argument("--date", help="Force date MM-DD")

    return parser.parse_args()


# =========================
# ENTRY POINT
# =========================

def main():
    args = parse_args()

    config = Config()
    config.TEST_MODE = args.test
    config.DRY_RUN = args.dry_run
    config.FORCE_DATE = args.date

    email_service = EmailService(config)
    birthday_service = BirthdayService(config, email_service)

    birthday_service.run()


if __name__ == "__main__":
    main()

