from http import HTTPMethod

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, request, jsonify

from config import settings
from form import pyform

app = Flask(__name__)


app.config['MAIL_SERVER'] = settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
app.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD.get_secret_value()
app.config['MAIL_DEFAULT_SENDER'] = settings.MAIL_USERNAME
app.config['MAIL_OWNER'] = settings.MAIL_OWNER


def send_email(subject, body, recipient):
    msg = MIMEMultipart()
    msg['From'] = settings.MAIL_USERNAME
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    try:
        with smtplib.SMTP( settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            # server.ehlo()
            # server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.auth_plain()
            server.sendmail(settings.MAIL_USERNAME, recipient, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route(rule="/contact", methods=[HTTPMethod.POST])
def send_message():
    result = pyform(data=request.form.to_dict())
    if isinstance(result, dict):
        user_email_subject = "Thank you for contacting us"
        user_email_body = (f"Hello {result.get('username')}, \n\n"
                           f"Thank you for reaching out to us. We have received your message and will review it shortly. "
                           f"We strive to provide prompt and quality service, so your inquiry will be addressed as soon as possible. "
                           f"If you have any further questions or additional information, please feel free to reach out to us. Best regards.")
        owner_email_subject = "Новый запрос со страницы"
        owner_email_body = (f"Получен новый запрос от {result.get('username')} ({result.get('email')}):\n\n"
                            f"Сообщение: {result.get('message')}")
        send_email(user_email_subject, user_email_body, result.get('email'))
        send_email(owner_email_subject, owner_email_body, settings.MAIL_OWNER)        
        return jsonify({})
    else:
        return result
