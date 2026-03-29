import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv(override=True)

def diag():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_SECRET")
    
    client = Client(api_key, api_secret, testnet=True)
    client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
    
    try:
        print("1. Testing account info (GET)...")
        client.futures_account()
        print("   SUCCESS! GET works.")
        
        print("\n2. Testing order placement (POST - MARKET BUY 0.001 BTC)...")
        # Placing a real order on testnet to confirm write permissions
        res = client.futures_create_order(
            symbol='BTCUSDT',
            side='BUY',
            type='MARKET',
            quantity=0.001
        )
        print(f"   SUCCESS! POST works. Order ID: {res['orderId']}")
        
    except BinanceAPIException as e:
        print(f"   FAILED: {e.code} - {e.message}")
        if e.code == -2015:
            print("\n!!! DIAGNOSIS !!!")
            print("Your API Key has READ permissions but NOT WRITE permissions for Futures.")
            print("Action: Go to testnet.binancefuture.com -> API Management -> Edit Restrictions")
            print("-> Check 'Enable Futures'.")
    except Exception as e:
        print(f"   UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    diag()
