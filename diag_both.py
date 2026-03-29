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
        print("Testing public futures_exchange_info()...")
        info = client.futures_exchange_info()
        symbols = [s['symbol'] for s in info['symbols'][:5]]
        print(f"SUCCESS! Public symbols: {symbols}")
        
        print("\nTesting private futures_account()...")
        client.futures_account()
        print("SUCCESS! Account info fetched.")
        
    except BinanceAPIException as e:
        print(f"ERROR: {e.code} - {e.message}")
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    diag()
