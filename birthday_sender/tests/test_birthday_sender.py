
import os
import json
import tempfile
from birthday_sender import Config, EmailService, BirthdayService

class DummyEmailService(EmailService):
    def __init__(self, config):
        super().__init__(config)
        self.sent = []

    def send(self, to_email, subject, html):
        self.sent.append(to_email)


def create_temp_birthdays(tmp_path):
    data = [
        {"name": "Test User", "email": "test@example.com", "month": 12, "day": 17}
    ]
    file_path = tmp_path / "birthdays.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return file_path


def test_email_sent_on_birthday(tmp_path):
    config = Config()
    config.BIRTHDAY_FILE = str(create_temp_birthdays(tmp_path))
    config.SENT_LOG_FILE = str(tmp_path / "sent_log.txt")
    config.DRY_RUN = True
    config.FORCE_DATE = "12-17"

    email_service = DummyEmailService(config)
    service = BirthdayService(config, email_service)

    service.run()

    assert "test@example.com" in email_service.sent


def test_no_duplicate_send(tmp_path):
    config = Config()
    config.BIRTHDAY_FILE = str(create_temp_birthdays(tmp_path))
    config.SENT_LOG_FILE = str(tmp_path / "sent_log.txt")
    config.FORCE_DATE = "12-17"

    email_service = DummyEmailService(config)
    service = BirthdayService(config, email_service)

    service.run()
    service.run()

    assert email_service.sent.count("test@example.com") == 1
