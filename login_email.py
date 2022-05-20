import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_sender = 'amitshproject@gmail.com'
email_receiver = 'ronen.halabi1@gmail.com'

subject = 'python!'

msg = MIMEMultipart()
msg['From'] = email_sender
msg['To'] = email_receiver
msg['Subject'] = subject

body = 'hi everyone ! this email is from python'
msg.attach(MIMEText(body, 'plain'))

#filename = 'Document.txt'
#attachment = open(filename, 'rb')
part = MIMEBase('application', 'octet_stream')

#part.set_payload((attachment).read())

#encoders.encode_base64(part)
#part.add_header('Content-Disposition', "attachment; filename= " + filename)
part.add_header('Content-Disposition', "ddd")

msg.attach(part)
text = msg.as_string()

connection = smtplib.SMTP('smtp.gmail.com', 587)
connection.starttls()
connection.login(email_receiver, 'ronen100')
connection.sendmail(email_receiver, email_receiver, text)
connection.quit()