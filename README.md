# Visa Appointment Checker

This project automates the process of checking for US visa appointment dates and sends alerts if an appointment is available within a specified date range.

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/visa-appointment-checker.git
   cd visa-appointment-checker
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install additional packages**

   ```bash
   pip install chromedriver-py smtplib
   ```

5. **Run the script**
   ```bash
   python3 main.py
   ```

## Configuration

Configure your login credentials and date range in `src/config.py`. Update the following fields with your information:

```python
# src/config.py

USERNAME = 'your_username'
PASSWORD = 'your_password'
START_DATE = 'YYYY-MM-DD'
END_DATE = 'YYYY-MM-DD'
EMAIL = 'your_email@example.com'
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_USERNAME = 'your_email_username'
EMAIL_PASSWORD = 'your_email_password'
```

## Tools Used

-  **Selenium**: For web automation and interaction with the visa appointment website.
-  **Chromedriver**: To control Chrome browser through Selenium.
-  **smtplib**: For sending email alerts when an appointment is available.

## Logic

1. **Login**: Automate the login process to the visa appointment website using Selenium.
2. **Check Availability**: Periodically check for available appointment dates within the specified date range.
3. **Send Alerts**: If an appointment is available within the date range, send an email alert to the specified email address.

## Code Usage

This code is intended for educational purposes only. Unauthorized use of this code to bypass any website's terms of service or to automate interactions with websites without permission is not encouraged and is solely the responsibility of the user. Use this tool responsibly and ensure that its usage complies with all relevant laws and terms of service.

## License

This project is licensed under the MIT License.
