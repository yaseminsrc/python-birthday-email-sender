# 🎉 Python Birthday Email Sender

A production-ready Python application that automatically sends birthday emails based on a JSON dataset.

The project is designed with clean architecture principles, testability, and real-world usage in mind.

---

## ✨ Features

- Automated birthday email sending
- Gmail SMTP integration
- Dry-run mode (no emails sent)
- Test mode for development
- Duplicate send prevention
- CLI interface
- Structured logging
- Unit tests with pytest
- Environment variable–based configuration

---

## 🧰 Technologies & Tools

### Programming Language
- **Python 3.11+**

### Core Libraries
- **smtplib** – SMTP email delivery
- **email.message** – MIME email construction
- **logging** – Structured application logging
- **json** – Data persistence
- **datetime** – Date handling

### Testing
- **pytest** – Unit testing framework
- **tempfile / tmp_path** – Isolated filesystem testing
- **Dependency Injection** – Mockable email service for tests

### Configuration & Security
- **Environment Variables** – Secure configuration management
- **.env / example.env** – Local environment setup

---

## 📂 Project Structure

```text
python-birthday-email-sender/
│
├── birthday_sender.py # Main application logic
├── birthdays.json # Birthday data
├── example.env # Environment variables example
├── .gitignore           # Git ignored files
├── tests/
│ └── test_birthday_sender.py
├── app.log # Runtime logs
└── PROJECT_DETAILS.md

```
---

### 🔐 Environment Variables

Create a `.env` file based on example.env:

```env
BIRTHDAY_EMAIL=yourgmail@gmail.com
BIRTHDAY_EMAIL_PASSWORD=your_app_password
```
> ⚠️ Use **Gmail App Password**, not your normal Gmail password.

---

### 🚀 Usage
Dry Run (no email sent)

```
python birthday_sender.py --dry-run
```
Test Mode
```
python birthday_sender.py --test
```
Force a Date
```
python birthday_sender.py --date 12-17
```
---

##  🧪 Run Tests

```
pytest
```
---

###  Run the application

```bash
python birthday_sender.py
```
---

## 🔐 Security Notes

* ❌ Never commit your `.env` file
* ✅ Always use Gmail App Passwords
* 🔄 Revoke and regenerate passwords if leaked

---

