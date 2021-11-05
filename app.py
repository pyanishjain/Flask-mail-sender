import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from flask import Flask, request, abort
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

# Email
SENDER = 'erickgross1994@gmail.com'
SENDERNAME = 'FLASK'
USERNAME_SMTP = "erickgross1994@gmail.com"
PASSWORD_SMTP = "ccjaoztxeaypwltm"
HOST = "smtp.gmail.com"
PORT = 587


# For sending Email in different Thread
class EmailThreading(threading.Thread):
    def __init__(self,SENDER,recipient,subject,body):
        self.SENDER = SENDER
        self.recipient = recipient
        self.subject = subject
        self.body = body
        threading.Thread.__init__(self)
    
    def run(self):
        self.send_email(self.SENDER,self.recipient,self.subject,self.body)


    def send_email(self,reply_to, recipient, subject, body):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = formataddr((SENDERNAME, SENDER))
        msg['To'] = recipient
        msg.add_header('Reply-To', reply_to)

        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        try:
            server = smtplib.SMTP(HOST, PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
            server.sendmail(SENDER, recipient, msg.as_string())
            server.close()
        except Exception as e:
            return False
        else:
            return True


@app.route('/', methods=['POST'])
def index():
    if not request.json:
        abort(400)
    data = request.json
    send = EmailThreading(SENDER,data['recipient'], data['subject'], data['body']).start()  
    return f'Message send: {send}', 201

if __name__ == '__main__':
    app.run(debug=False)
