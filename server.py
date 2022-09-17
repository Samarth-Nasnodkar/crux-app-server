from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask

cred = credentials.Certificate("./creds.json")
firebase_admin.initialize_app(cred)

# app = Flask(__name__)
client = firestore.client()

coins = [
    {
        "name": "Doge",
        "tag": "DOGE",
        "icon": "assets/images/doge.png",
        "price": 20.5,
        "gain": 0.41,
        "top": datetime.now()
    },
    {
        "name": "Shiba Inu",
        "tag": "SHIB",
        "icon": "assets/images/doge.png",
        "price": 0.04,
        "gain": 0.3,
        "top": datetime.now()
    },
    {
        "name": "Avalanche",
        "tag": "AVAX",
        "icon": "assets/images/avax.png",
        "price": 1052,
        "gain": 1.3,
        "top": datetime.now()
    }
]

for coin in coins:
    client.collection('coins').add(
        coin
    )
