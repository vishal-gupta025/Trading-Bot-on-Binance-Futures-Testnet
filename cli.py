import os
import argparse
from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.orders import place_order, format_result
from bot.validators import (validate_symbol, validate_side, 
                            validate_order_type, validate_quantity, validate_price)
from bot.logging_config import setup_logging

# Load .env file
load_dotenv()


def main():
    # Setup logging
    setup_logging()
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )
    parser.add_argument("--symbol", "-s", required=True, 
                        help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", "-S", required=True,
                        help="Order side: BUY or SELL")
    parser.add_argument("--type", "-t", dest="order_type", required=True,
                        help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", "-q", required=True,
                        help="Order quantity")
    parser.add_argument("--price", "-p", default=None,
                        help="Order price (required for LIMIT)")
    
    args = parser.parse_args()
    
    # Validate inputs
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
    except ValueError as e:
        print(f"\nValidation Error: {e}")
        return
    
    # Check credentials
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        print("\nError: Set BINANCE_API_KEY and BINANCE_API_SECRET in .env file")
        return
    
    # Print order request
    print("\n" + "=" * 50)
    print("ORDER REQUEST")
    print("=" * 50)
    print(f"  Symbol:   {symbol}")
    print(f"  Side:     {side}")
    print(f"  Type:     {order_type}")
    print(f"  Quantity: {quantity}")
    if price:
        print(f"  Price:    {price}")
    print("=" * 50)
    
    # Place order
    client = BinanceClient(api_key, api_secret)
    result = place_order(client, symbol, side, order_type, quantity, price)
    
    # Print result
    print(format_result(result))


if __name__ == "__main__":
    main()
