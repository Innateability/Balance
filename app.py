from flask import Flask, jsonify
import requests
import time
import hmac
import hashlib
import os

app = Flask(__name__)

API_KEY = os.environ.get('BYBIT_API_KEY')
API_SECRET = os.environ.get('BYBIT_API_SECRET')

@app.route('/')
def home():
    return "Bybit TRXUSDT Position Web Service"

@app.route('/position')
def get_trxusdt_position():
    url = 'https://api.bybit.com/v5/position/list'

    params = {
        'category': 'linear',
        'symbol': 'TRXUSDT'
    }

    timestamp = str(int(time.time() * 1000))
    recv_window = '5000'
    query_string = f"category=linear&symbol=TRXUSDT"
    to_sign = timestamp + API_KEY + recv_window + query_string
    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        to_sign.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    headers = {
        'X-BYBIT-API-KEY': API_KEY,
        'X-BYBIT-API-SIGN': signature,
        'X-BYBIT-API-TIMESTAMP': timestamp,
        'X-BYBIT-API-RECV-WINDOW': recv_window
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            positions = data['result']['list']
            if not positions:
                return jsonify({"contracts": 0, "message": "No open position."})
            size = float(positions[0]['size'])
            return jsonify({"contracts": size})
        except Exception as e:
            return jsonify({"error": "Parsing error", "details": str(e)})
    else:
        return jsonify({"error": "API call failed", "details": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
