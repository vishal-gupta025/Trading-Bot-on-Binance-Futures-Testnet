import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Testnet base URL
TESTNET_URL = "https://testnet.binancefuture.com"

logger = logging.getLogger("trading_bot")


class BinanceClient:
    
    def __init__(self, api_key: str, api_secret: str):
        self.client = Client(api_key, api_secret, testnet=True)
        # Set futures testnet URL
        self.client.FUTURES_URL = TESTNET_URL
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                    quantity: float, price: float = None) -> dict:
        
        logger.info(f"Placing {order_type} {side} order: {quantity} {symbol}" +
                   (f" @ {price}" if price else ""))
        
        try:
            if order_type == "MARKET":
                response = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            else:  # LIMIT
                response = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity,
                    price=price,
                    timeInForce="GTC"
                )
            
            logger.debug(f"Response: {response}")
            return response
            
        except BinanceAPIException as e:
            logger.error(f"API Error: {e.message}")
            raise Exception(f"API Error: {e.message}")
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise
