"""Module processing app"""

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from form import pyform

app = Flask(__name__)
mail = Mail()
mail.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ilya06041994@gmail.com'
app.config['MAIL_PASSWORD'] = '336062072ilya'
app.config['MAIL_DEFAULT_SENDER'] = 'ilya06041994@gmail.com'


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route("/contact", methods=['POST', 'GET'])
def process_form():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        message = request.form["message"]
        form_data = {"username": username, "email": email, "message": message}
        result = pyform(form_data)
        if isinstance(result, dict) and 'username' in result and 'email' in result and 'message' in result:
            return jsonify(result)
        return result
        

@app.route("/send", methods=['POST'])
def send_message():
    form_data = request.json
    result = pyform(form_data)
    if isinstance(result, dict) and 'username' in result and 'email' in result and 'message' in result:
        username = result['username']
        email = result['email']
        user_message = result['message']
        message = Message(
            subject="Thank you for contacting us",
            body=f"Hello {username}, \n\n" 
            f"Thank you for reaching out to us. We have received your \n\n" 
            f"message and will review it shortly. We strive to provide \n\n"
            f"prompt and quality service, so your inquiry will be addressed \n\n"
            f"as soon as possible. If you have any further questions or additional \n\n"
            f"information, please feel free to reach out to us. Best regards.",
            sender="ilya06041994@gmail.com",
            recipients=[email]
        )
    mail.send(message)
  
if __name__ == '__main__':
    app.run(debug=True)