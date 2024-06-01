"""Module processing app"""

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from form import pyform

app = Flask(__name__)


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
        print(result)
        if isinstance(result, dict) and 'username' in result and 'email' in result and 'message' in result:
            return jsonify(result)
        return result
        
        
if __name__ == '__main__':
    app.run(debug=True)