from http import HTTPMethod

from flask import Flask, render_template, request, jsonify
import aio_smtp

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


smtp_client = aio_smtp.SMTP(
    host=app.config['MAIL_SERVER'],
    port=app.config['MAIL_PORT'],
    start_tls=app.config['MAIL_USE_TLS'],
    username=app.config['MAIL_USERNAME'],
    password=app.config['MAIL_PASSWORD']
)

@app.route('/')
def homepage():
    return render_template("index.html")


@app.route(rule="/contact", methods=[HTTPMethod.POST])
async def send_message():
    result = pyform(data=request.form.to_dict())
    if isinstance(result, dict):
        message = aio_smtp.Message(
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
        owner_message = aio_smtp.Message(
            subject="Новый запрос со страницы",
            body=f"Получен новый запрос от {result.get('username')} ({result.get('email')}):\n\n"
                 f"Сообщение: {result.get('message')}",
            sender=settings.MAIL_USERNAME,
            recipients=[settings.MAIL_OWNER]  # Здесь укажите email владельца
        )
        await smtp_client.send(message)
        await smtp_client.send(owner_message)
        return jsonify({})
    else:
        return result
