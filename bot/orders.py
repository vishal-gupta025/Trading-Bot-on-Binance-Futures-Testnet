"""
Order placement logic
"""

import logging

logger = logging.getLogger("trading_bot")


def place_order(client, symbol: str, side: str, order_type: str, 
                quantity: float, price: float = None) -> dict:
    """
    Place an order and handle the response.
    
    Returns:
        dict with order details or error
    """
    try:
        response = client.place_order(symbol, side, order_type, quantity, price)
        
        logger.info(f"Order placed successfully. ID: {response.get('orderId')}")
        
        return {
            "success": True,
            "orderId": response.get("orderId"),
            "symbol": response.get("symbol"),
            "side": response.get("side"),
            "type": response.get("type"),
            "status": response.get("status"),
            "quantity": response.get("origQty"),
            "executedQty": response.get("executedQty"),
            "price": response.get("price"),
            "avgPrice": response.get("avgPrice")
        }
        
    except Exception as e:
        logger.error(f"Order failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def format_result(result: dict) -> str:
    """Format order result for display."""
    lines = ["\n" + "=" * 50]
    
    if result["success"]:
        lines.append("ORDER RESPONSE DETAILS")
        lines.append("=" * 50)
        lines.append(f"  Order ID:      {result['orderId']}")
        lines.append(f"  Status:        {result['status']}")
        lines.append(f"  Executed Qty:  {result['executedQty']}")
        if result.get('avgPrice'):
            lines.append(f"  Avg Price:     {result['avgPrice']}")
        lines.append("-" * 50)
        lines.append("  SUCCESS: Order placed successfully!")
    else:
        lines.append("ORDER FAILED")
        lines.append("=" * 50)
        lines.append(f"  Error: {result['error']}")
        lines.append("-" * 50)
        lines.append("  FAILURE: Order was not placed.")
    
    lines.append("=" * 50)
    return "\n".join(lines)
