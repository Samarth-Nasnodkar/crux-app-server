import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask

cred = credentials.Certificate("./creds.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
client = firestore.client()


@app.route('/')
def home():
    return 'Hello!'


app.run(host='0.0.0.0', port=8080)
