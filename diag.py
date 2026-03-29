import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv(override=True)

def diag():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_SECRET")
    
    print(f"API Key: {api_key[:5]}...{api_key[-5:]}")
    
    client = Client(api_key, api_secret, testnet=True)
    
    # Check current URLs in the library
    print(f"Base API URL: {client.API_URL}")
    print(f"Futures URL: {client.FUTURES_URL}")
    
    try:
        # Try fetching account info
        print("\nAttempting to fetch futures account info...")
        acc = client.futures_account()
        print("SUCCESS! Account assets overview:")
        for asset in acc['assets'][:5]:
            if float(asset['walletBalance']) > 0:
                print(f" - {asset['asset']}: {asset['walletBalance']}")
                
    except BinanceAPIException as e:
        print(f"\nFAILED with code {e.code}: {e.message}")
        if e.code == -2015:
            print("REASON: Invalid API Key. This usually means:")
            print("1. Using Spot testnet keys on Futures testnet.")
            print("2. The keys are expired or deleted.")
            print("3. Wrong domain (the library is hitting production by mistake).")
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {str(e)}")

if __name__ == "__main__":
    diag()
