"""
Input validation functions
"""


def validate_symbol(symbol: str) -> str:
    """Validate and normalize trading symbol."""
    if not symbol:
        raise ValueError("Symbol is required")
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        raise ValueError("Symbol must be a USDT pair (e.g., BTCUSDT)")
    return symbol


def validate_side(side: str) -> str:
    """Validate order side."""
    if not side:
        raise ValueError("Side is required")
    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    """Validate order type."""
    if not order_type:
        raise ValueError("Order type is required")
    order_type = order_type.upper().strip()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT")
    return order_type


def validate_quantity(quantity) -> float:
    """Validate order quantity."""
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        return qty
    except (TypeError, ValueError):
        raise ValueError("Invalid quantity")


def validate_price(price, order_type: str) -> float:
    """Validate order price."""
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError("Price must be positive")
            return p
        except (TypeError, ValueError):
            raise ValueError("Invalid price")
    return None
