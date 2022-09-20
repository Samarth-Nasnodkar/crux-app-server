from datetime import datetime
from multiprocessing.dummy import Process
import random
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./creds.json")
firebase_admin.initialize_app(cred)

client = firestore.client()

BASE_PRICES = []

# coins = [
#     {
#         "name": "Doge",
#         "tag": "DOGE",
#         "icon": "assets/images/doge.png",
#         "price": 20.5,
#         "gain": 0.41,
#         "prices": [],
#         "top": datetime.now()
#     },
#     {
#         "name": "Shiba Inu",
#         "tag": "SHIB",
#         "icon": "assets/images/shib.png",
#         "price": 215,
#         "gain": 0.3,
#         "prices": [],
#         "top": datetime.now()
#     },
#     {
#         "name": "Avalanche",
#         "tag": "AVAX",
#         "icon": "assets/images/avax.png",
#         "price": 1052,
#         "gain": 1.3,
#         "prices": [],
#         "top": datetime.now()
#     }
# ]

coins = []
coin_names = ['DOGE', 'SHIB', 'AVAX']
print('Fetching initial data...')
for ind, coin_name in enumerate(coin_names):
    data = client.collection('coins').document(coin_name).get().to_dict()
    coins.append(data)
    BASE_PRICES.append(data['price'])
print('Fetched initial data!')

for coin in coins:
    coin['prices'] = []


def generate_new_price(old_price: float):
    up_or_down = random.randint(0, 1)
    price_delta = random.random() * 0.02
    if up_or_down == 0:
        return old_price + (price_delta * old_price)
    else:
        return old_price - (price_delta * old_price)


def update_prices():
    while True:
        for ind, coin in enumerate(coins):
            coin['price'] = round(generate_new_price(coin['price']), 2)
            coin['gain'] = round((coin['price'] - BASE_PRICES[ind]) / 100, 2)
            coin['prices'].append({
                'ts': datetime.now(),
                'price': coin['price'],
            })
            client.collection('coins').document(coin['tag']).update({
                'price': coin["price"],
                'gain': coin['gain'],
                'prices': coin['prices'],
            })
            # print(f'New price of {coin["name"]} = {coin["price"]}')

        time.sleep(1)


if __name__ == '__main__':
    print('Starting Server...')
    p = Process(target=update_prices)
    p.start()

    while True:
        time.sleep(60)
