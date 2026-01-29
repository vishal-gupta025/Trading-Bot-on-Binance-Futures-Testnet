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
        lines.append("ORDER PLACED SUCCESSFULLY")
        lines.append("=" * 50)
        lines.append(f"  Order ID:     {result['orderId']}")
        lines.append(f"  Symbol:       {result['symbol']}")
        lines.append(f"  Side:         {result['side']}")
        lines.append(f"  Type:         {result['type']}")
        lines.append(f"  Status:       {result['status']}")
        lines.append(f"  Quantity:     {result['quantity']}")
        lines.append(f"  Executed:     {result['executedQty']}")
        if result.get('price') and result['price'] != '0.00':
            lines.append(f"  Price:        {result['price']}")
        if result.get('avgPrice') and result['avgPrice'] != '0.00':
            lines.append(f"  Avg Price:    {result['avgPrice']}")
    else:
        lines.append("ORDER FAILED")
        lines.append("=" * 50)
        lines.append(f"  Error: {result['error']}")
    
    lines.append("=" * 50)
    return "\n".join(lines)
