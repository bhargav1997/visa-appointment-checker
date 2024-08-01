import smtplib
from twilio.rest import Client
import src.config as config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import src.config as config

def send_email():
    msg = MIMEMultipart()
    msg['From'] = config.EMAIL
    msg['To'] = config.RECIPIENT_EMAIL
    msg['Subject'] = "Visa Appointment Available"

    body = "An appointment is available within your specified range."
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(config.EMAIL, config.EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(config.EMAIL, config.RECIPIENT_EMAIL, text)

def send_sms():
    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body="Visa Appointment Available",
        from_=config.TWILIO_PHONE_NUMBER,
        to=config.RECIPIENT_PHONE_NUMBER
    )
