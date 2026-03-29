import sys
import argparse
from bot.logging_config import logger
from bot.client import BinanceClient, BinanceAPIError, NetworkError
from bot.validators import (
    validate_symbol, 
    validate_side, 
    validate_order_type, 
    validate_quantity, 
    validate_price
)
from bot.orders import place_order

def print_order_success_table(order: dict):
    """
    Prints a formatted ASCII table of the successfully placed order.
    
    Args:
        order (dict): The API response from Binance.
    """
    # Extract data for display from the response
    order_id = str(order.get('orderId', 'N/A'))
    symbol = str(order.get('symbol', 'N/A'))
    side = str(order.get('side', 'N/A'))
    order_type = str(order.get('type', 'N/A'))
    status = str(order.get('status', 'NEW'))
    executed_qty = str(order.get('executedQty', '0.000'))
    avg_price = str(order.get('avgPrice', '0.0'))
    
    # ASCII table content
    print("╔══════════════════════════════╗")
    print("║     ORDER PLACED SUCCESSFULLY ║")
    print("╠══════════════════════════════╣")
    print(f"║ Order ID   : {order_id:<17} ║")
    print(f"║ Symbol     : {symbol:<17} ║")
    print(f"║ Side       : {side:<17} ║")
    print(f"║ Type       : {order_type:<17} ║")
    print(f"║ Status     : {status:<17} ║")
    print(f"║ Executed   : {executed_qty:<17} ║")
    print(f"║ Avg Price  : {avg_price:<17} ║")
    print("╚══════════════════════════════╝")

def main():
    """
    Main entry point for the trading bot CLI.
    Parses arguments, validates inputs, and executes order placement.
    """
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="CLI Support for Binance Futures Testnet Order Placement.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Market BUY order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Limit SELL order
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 80000
        """
    )
    
    # Required arguments
    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, help="Order side (BUY or SELL)")
    parser.add_argument("--type", required=True, dest="order_type", help="Order type (MARKET or LIMIT)")
    parser.add_argument("--quantity", required=True, help="Order quantity (positive float)")
    
    # Optional arguments
    parser.add_argument("--price", help="Order price (required for LIMIT orders)")
    
    args = parser.parse_args()
    
    try:
        # Step 1: Input Validation
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
        
        # Step 2: Initialize Client and Execute Order
        client = BinanceClient()
        order_response = place_order(client, symbol, side, order_type, quantity, price)
        
        # Step 3: Print formatted success message
        print_order_success_table(order_response)
        
    except ValueError as e:
        # Handle validation errors
        print(f"[ERROR] Validation Failed: {str(e)}")
        sys.exit(1)
        
    except (BinanceAPIError, NetworkError) as e:
        # Handle API or Network failures
        print(f"[ERROR] API Request Failed: {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        # Catch-all for unexpected errors
        print(f"[ERROR] Unexpected Error: {str(e)}")
        logger.exception("Unexpected exception occurred in CLI main.")
        sys.exit(1)

if __name__ == "__main__":
    main()
