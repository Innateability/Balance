import requests
import time
import hmac
import hashlib

# Replace with your Bybit API credentials
API_KEY = 'your_api_key_here'
API_SECRET = 'your_api_secret_here'

def get_trxusdt_position():
    url = 'https://api.bybit.com/v5/position/list'

    # Query params
    params = {
        'category': 'linear',         # 'linear' for USDT perpetual
        'symbol': 'TRXUSDT'
    }

    # Prepare signature
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
                print("No open position for TRXUSDT.")
                return 0
            size = float(positions[0]['size'])
            print(f"Open TRXUSDT contracts: {size}")
            return size
        except Exception as e:
            print("Error parsing response:", e)
    else:
        print("API error:", response.status_code, response.text)

    return 0

# Run it
get_trxusdt_position(
