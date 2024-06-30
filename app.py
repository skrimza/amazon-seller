from http import HTTPMethod, client
import json

from flask import Flask, render_template, request, jsonify

from config import settings
from form import pyform

app = Flask(__name__)

app.config['ID_OWNER'] = settings.ID_OWNER.get_secret_value()
app.config['BOT_TOKEN'] = settings.BOT_TOKEN.get_secret_value()


def send_message_telegram(chat_id, text):
    telegram_connect = client.HTTPConnection("api.telegram.org")
    headers = {'Content-type': 'application/json'}
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    json_data = json.dumps(payload)
    conn = client.HTTPSConnection("api.telegram.org")
    conn.request("POST", f"/bot{settings.BOT_TOKEN}/sendMessage", json_data, headers)
    
    response = conn.getresponse()
    data = response.read()
    
    conn.close()
    return json.loads(data)
        

@app.route('/')
def homepage():
    return render_template("index.html")


@app.route(rule="/contact", methods=[HTTPMethod.POST])
def send_message():
    result = pyform(data=request.form.to_dict())
    if isinstance(result, dict):
        owner_data_body = (f"New request from the website:\n Name: {result.get('username')},\n email: ({result.get('email')}):\n\n"
                            f"text: {result.get('message')}")
        response = send_message_telegram(settings.ID_OWNER, owner_data_body)        
        return jsonify(response)
    else:
        return result
