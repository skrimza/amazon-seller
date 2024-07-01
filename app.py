from http import HTTPMethod, client
import json
from urllib import parse

from flask import Flask, render_template, request, jsonify

from config import settings
from form import pyform

app = Flask(__name__)

app.config['ID_OWNER'] = settings.ID_OWNER
app.config['BOT_TOKEN'] = settings.BOT_TOKEN.get_secret_value()


def get_updates():
    offset=0
    headers = {'Content-type': 'application/json'}
    conn = client.HTTPSConnection("api.telegram.org")
    conn.request(HTTPMethod.POST, f"/bot{settings.BOT_TOKEN}/getUpdates", offset, headers=headers)



def send_message_telegram(text):
    get_updates()
    headers = {'Content-type': 'application/json'}
    payload = {
        'chat_id': settings.ID_OWNER,
        'text': text
    }
    json_data = json.dumps(payload)
    conn = client.HTTPSConnection("api.telegram.org")
    conn.request(HTTPMethod.POST, f"/bot{settings.BOT_TOKEN}/sendMessage", json_data, headers=headers)
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
        response = send_message_telegram(parse.quote(owner_data_body))        
        return jsonify(response)
    else:
        return result