import smtplib
from email.mime.text import MIMEText

msg = MIMEText("I am MAMURAI")
msg['Subject'] = "AN Email Alert"
msg['From'] = "gohome.x105.gn@gmail.com"
msg['To'] = "gohome.x105.gn@gmail.com"

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()