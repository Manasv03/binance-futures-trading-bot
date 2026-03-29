from bot.client import BinanceClient, BinanceAPIError, NetworkError
from bot.logging_config import logger

def place_order(client: BinanceClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    """
    Constructs and places an order on the Binance Futures Testnet.
    
    Args:
        client (BinanceClient): Initialized Binance client.
        symbol (str): Trading pair (e.g., BTCUSDT).
        side (str): BUY or SELL.
        order_type (str): MARKET or LIMIT.
        quantity (float): Order quantity.
        price (float, optional): Order price for LIMIT orders.
        
    Returns:
        dict: The API response for the placed order.
        
    Raises:
        BinanceAPIError: If the API returns an error.
        NetworkError: If a connection issues occurs.
        ValueError: If parameters are logically incorrect.
    """
    # Base parameters for all order types
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }
    
    # Extra parameters for LIMIT orders
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price must be provided for LIMIT orders.")
        
        params["price"] = price
        params["timeInForce"] = "GTC"  # Good 'Till Cancelled
        
    # Log a human-readable summary
    price_info = f"Price: {price}" if price else "Price: N/A (MTM)"
    logger.info(f"Placing {order_type} {side} order | Symbol: {symbol} | Qty: {quantity} | {price_info}")
    
    try:
        # Send the POST request to the correct endpoint
        response = client.post_order("/fapi/v1/order", params)
        
        # Log success and return the response
        logger.info(f"Order successfully placed! Order ID: {response.get('orderId')}")
        return response
        
    except (BinanceAPIError, NetworkError) as e:
        # Log the failure before re-raising
        logger.error(f"Failed to place order: {str(e)}")
        raise e
