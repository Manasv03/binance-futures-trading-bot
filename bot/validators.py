import re

def validate_symbol(symbol: str) -> str:
    """
    Validates the trading symbol. Must be uppercase, alphanumeric, and end with USDT or BUSD.
    
    Args:
        symbol (str): The symbol to validate.
        
    Returns:
        str: The validated uppercase symbol.
        
    Raises:
        ValueError: If the symbol is invalid.
    """
    if not symbol:
        raise ValueError("Symbol is required")
    
    symbol = symbol.strip().upper()
    
    # Binance symbols are alphanumeric and typically end with a quote currency like USDT or BUSD
    pattern = r'^[A-Z0-9]+(USDT|BUSD)$'
    if not re.match(pattern, symbol):
        raise ValueError(f"Invalid symbol: '{symbol}'. Must be alphanumeric and end with USDT or BUSD.")
        
    return symbol

def validate_side(side: str) -> str:
    """
    Validates the order side. Must be BUY or SELL.
    
    Args:
        side (str): The side to validate.
        
    Returns:
        str: The validated uppercase side.
        
    Raises:
        ValueError: If the side is invalid.
    """
    if not side:
        raise ValueError("Side is required")
        
    side = side.strip().upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: '{side}'. Must be BUY or SELL.")
        
    return side

def validate_order_type(order_type: str) -> str:
    """
    Validates the order type. Must be MARKET or LIMIT.
    
    Args:
        order_type (str): The type to validate.
        
    Returns:
        str: The validated uppercase order type.
        
    Raises:
        ValueError: If the order type is invalid.
    """
    if not order_type:
        raise ValueError("Order type is required")
        
    order_type = order_type.strip().upper()
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValueError(f"Invalid order type: '{order_type}'. Must be MARKET or LIMIT.")
        
    return order_type

def validate_quantity(qty: str) -> float:
    """
    Validates the order quantity. Must be a positive float.
    
    Args:
        qty (str): The quantity to validate.
        
    Returns:
        float: The validated float quantity.
        
    Raises:
        ValueError: If the quantity is non-numeric or <= 0.
    """
    if qty is None:
        raise ValueError("Quantity is required")
        
    try:
        f_qty = float(qty)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid quantity: '{qty}'. Must be a numeric value.")
        
    if f_qty <= 0:
        raise ValueError(f"Invalid quantity: {f_qty}. Must be greater than 0.")
        
    return f_qty

def validate_price(price: str, order_type: str) -> float or None:
    """
    Validates the order price. 
    If order_type is LIMIT: price must be provided and be a positive float.
    If order_type is MARKET: price is ignored (return None).
    
    Args:
        price (str): The price to validate.
        order_type (str): The type of the order.
        
    Returns:
        float or None: The validated float price or None.
        
    Raises:
        ValueError: If price is missing for LIMIT or is invalid.
    """
    if order_type.upper() == 'MARKET':
        return None
        
    if price is None:
        raise ValueError("Price is required for LIMIT orders.")
        
    try:
        f_price = float(price)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid price: '{price}'. Must be a numeric value.")
        
    if f_price <= 0:
        raise ValueError(f"Invalid price: {f_price}. Must be greater than 0.")
        
    return f_price
