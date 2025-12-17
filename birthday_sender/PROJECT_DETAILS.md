# 🎉 Python Birthday Email Sender

Automated Python script that sends birthday emails using Gmail SMTP with secure environment variables.

---

## ✨ Features

* 📧 Automated birthday email sending
* 🔐 Secure credential handling with environment variables (`.env`)
* 📄 JSON-based birthday list management
* 🚫 Prevents duplicate emails on the same day
* 🧪 Test mode for safe local testing
* 💻 Works on Windows, macOS, and Linux

---

## 🛠️ Tech Stack

* **Python 3.9+**
* `smtplib`
* `email.message`
* `datetime`
* Gmail SMTP

---

## 📂 Project Structure

```text
python-birthday-email-sender/
│
├── birthday_sender.py   # Main application logic
├── birthdays.json       # Birthday data
├── example.env          # Environment variable example
├── .gitignore           # Git ignored files
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/python-birthday-email-sender.git
cd python-birthday-email-sender
```

### 2️⃣ Create `.env` file

Copy the example file:

```bash
cp example.env .env
```

Edit `.env` and add your credentials:

```env
BIRTHDAY_EMAIL=yourgmail@gmail.com
BIRTHDAY_EMAIL_PASSWORD=your_app_password
```

> ⚠️ Use **Gmail App Password**, not your normal Gmail password.

---

### 3️⃣ Configure birthdays

Edit `birthdays.json`:

```json
[
  {
    "name": "John Doe",
    "email": "john@example.com",
    "month": 12,
    "day": 17
  }
]
```

---

### 4️⃣ Run the application

```bash
python birthday_sender.py
```

---

## 🧪 Test Mode

Enable test mode inside `birthday_sender.py`:

```python
TEST_MODE = True
```

* No emails will be sent
* Actions will be printed to the console

---

## 🔐 Security Notes

* ❌ Never commit your `.env` file
* ✅ Always use Gmail App Passwords
* 🔄 Revoke and regenerate passwords if leaked

---

## ⏰ Automation

You can schedule the script to run daily using:

* **Windows Task Scheduler**
* **cron (Linux / macOS)**

---

## 📈 Project Level

This project is suitable for **Junior+ to Mid-level Python developers**, demonstrating:

* Automation scripting
* Secure configuration handling
* File-based data management
* Basic production readiness
