import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET")

client = Client(api_key, api_secret, testnet=True)
client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

print(f"DEBUG: client.API_URL      = {client.API_URL}")
print(f"DEBUG: client.FUTURES_URL  = {client.FUTURES_URL}")

try:
    print("Testing futures_account()...")
    client.futures_account()
    print("Account info fetched successfully.")
except BinanceAPIException as e:
    print(f"ERROR: {e.code} - {e.message}")
except Exception as e:
    print(f"UNEXPECTED ERROR: {type(e).__name__}: {str(e)}")
