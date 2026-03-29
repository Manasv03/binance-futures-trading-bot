import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from bot.logging_config import logger

# Load environment variables from .env file
load_dotenv(override=True)

class BinanceAPIError(Exception):
    """Exception raised for errors returned by the Binance API."""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"BinanceAPIError(code={code}): {message}")

class NetworkError(Exception):
    """Exception raised for network-related failures."""
    def __init__(self, message):
        self.message = message
        super().__init__(f"NetworkError: {message}")

class BinanceClient:
    """
    A client wrapper for the Binance Futures Testnet using python-binance library.
    Handles communication with Binance and error translation.
    """
    
    def __init__(self):
        """
        Initializes the BinanceClient with credentials from environment variables.
        Sets up the python-binance Client with testnet=True.
        """
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_SECRET")
        
        if not self.api_key or not self.api_secret:
            logger.error("Missing BINANCE_API_KEY or BINANCE_SECRET in environment variables.")
            raise ValueError("API credentials not found. Please check your .env file.")

        try:
            # Initialize the python-binance Client for Testnet
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            
            # Explicitly set Futures Testnet URL (sometimes needed in python-binance)
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            
        except Exception as e:
            logger.error(f"Failed to initialize Binance Client: {str(e)}")
            raise NetworkError(f"Initialization error: {str(e)}")

    def post_order(self, endpoint: str, params: dict) -> dict:
        """
        Sends a POST request to Binance Futures to create an order.
        For signature compatibility, 'endpoint' is accepted but ignored as 
        the library handles routing.
        
        Args:
            endpoint (str): Ignored (kept for signature compatibility).
            params (dict): The order parameters.
            
        Returns:
            dict: The JSON response from Binance.
            
        Raises:
            BinanceAPIError: If the API returns an error structure.
            NetworkError: If a connection or timeout occurs.
        """
        # Prepare masked params for logging (hide sensitive info if any)
        masked_params = params.copy()
        
        logger.debug(f"Request Params: {masked_params}")
        
        try:
            # Send the request using python-binance futures_create_order
            # This handles signing, timestamping, and HTTP POST automatically
            response = self.client.futures_create_order(**params)
            
            # Log the response content for debugging
            logger.debug(f"API Response: {response}")
            
            return response
            
        except BinanceAPIException as e:
            # Catch the library's specific API exception and translate it to our custom error
            logger.error(f"Binance API returned an error: {e.status_code} - {e.message}")
            raise BinanceAPIError(e.code, e.message)
            
        except Exception as e:
            # Catch all other exceptions (network, timeout, etc.) as NetworkError
            logger.error(f"An unexpected error occurred during API call: {str(e)}")
            raise NetworkError(f"Network error: {str(e)}")
