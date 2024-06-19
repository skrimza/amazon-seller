from http import HTTPMethod

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

from config import settings
from form import pyform

app = Flask(__name__)
mail = Mail()
mail.init_app(app)

app.config['MAIL_SERVER'] = settings.MAIL_SERVER
app.config['MAIL_PORT'] = settings.MAIL_PORT
app.config['MAIL_USE_TLS'] = settings.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = settings.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD.get_secret_value()
app.config['MAIL_DEFAULT_SENDER'] = settings.MAIL_USERNAME
app.config['MAIL_OWNER'] = settings.MAIL_OWNER


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route(rule="/contact", methods=[HTTPMethod.POST])
def send_message():
    result = pyform(data=request.form.to_dict())
    if isinstance(result, dict):
        message = Message(
            subject="Thank you for contacting us",
            body=f"Hello {result.get('username')}, \n\n"
                 f"Thank you for reaching out to us. We have received your \n\n"
                 f"message and will review it shortly. We strive to provide \n\n"
                 f"prompt and quality service, so your inquiry will be addressed \n\n"
                 f"as soon as possible. If you have any further questions or additional \n\n"
                 f"information, please feel free to reach out to us. Best regards.",
            sender=settings.MAIL_USERNAME,
            recipients=[result.get('email')]
        )
        owner_message = Message(
            subject="Новый запрос со страницы",
            body=f"Получен новый запрос от {result.get('username')} ({result.get('email')}):\n\n"
                 f"Сообщение: {result.get('message')}",
            sender=settings.MAIL_USERNAME,
            recipients=[settings.MAIL_OWNER]  # Здесь укажите email владельца
        )
        return jsonify({})
        mail.send(message)
        mail.send(owner_message)
    else:
        return result
