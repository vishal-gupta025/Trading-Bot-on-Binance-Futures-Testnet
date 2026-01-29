import streamlit as st
import os
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.orders import place_order
from bot.logging_config import setup_logging

# Load environment
load_dotenv()
setup_logging()

# Page config
st.set_page_config(
    page_title="Trading Bot",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Binance Futures Trading Bot")
st.caption("Testnet Trading Interface")

# Initialize client
@st.cache_resource
def get_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        return None
    return BinanceClient(api_key, api_secret)

client = get_client()

if not client:
    st.error("❌ API keys not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file.")
    st.stop()

st.success("✅ Connected to Binance Futures Testnet")

# Order Form
st.header("Place Order")

col1, col2 = st.columns(2)

with col1:
    symbol = st.text_input("Symbol", value="BTCUSDT", help="Trading pair (e.g., BTCUSDT, ETHUSDT)")
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])

with col2:
    side = st.selectbox("Side", ["BUY", "SELL"])
    quantity = st.number_input("Quantity", min_value=0.001, value=0.002, step=0.001, format="%.3f")

# Price input for LIMIT orders
price = None
if order_type == "LIMIT":
    price = st.number_input("Price (USDT)", min_value=0.01, value=80000.0, step=100.0, format="%.2f")

# Order summary
st.divider()
st.subheader("Order Summary")

summary_col1, summary_col2 = st.columns(2)
with summary_col1:
    st.write(f"**Symbol:** {symbol}")
    st.write(f"**Side:** {side}")
with summary_col2:
    st.write(f"**Type:** {order_type}")
    st.write(f"**Quantity:** {quantity}")
    if order_type == "LIMIT":
        st.write(f"**Price:** ${price:,.2f}")

# Place Order Button
st.divider()
if st.button("🚀 Place Order", type="primary", use_container_width=True):
    with st.spinner("Placing order..."):
        result = place_order(client, symbol.upper(), side, order_type, quantity, price)
    
    if result["success"]:
        st.success("✅ Order Placed Successfully!")
        st.json({
            "Order ID": result["orderId"],
            "Status": result["status"],
            "Executed Qty": result["executedQty"],
            "Avg Price": result["avgPrice"]
        })
    else:
        st.error(f"❌ Order Failed: {result['error']}")

# Recent Orders Section
st.divider()
st.header("Recent Orders")

if st.button("🔄 Refresh Orders"):
    st.rerun()

try:
    orders = client.client.futures_get_all_orders(symbol="BTCUSDT", limit=5)
    if orders:
        for order in reversed(orders):
            with st.expander(f"Order #{order['orderId']} - {order['side']} {order['type']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Symbol:** {order['symbol']}")
                    st.write(f"**Side:** {order['side']}")
                    st.write(f"**Type:** {order['type']}")
                with col2:
                    st.write(f"**Status:** {order['status']}")
                    st.write(f"**Quantity:** {order['origQty']}")
                    st.write(f"**Avg Price:** ${float(order['avgPrice']):,.2f}")
    else:
        st.info("No recent orders found.")
except Exception as e:
    st.warning(f"Could not fetch orders: {e}")

# Footer
st.divider()
st.caption("💡 This bot connects to Binance Futures Testnet. No real funds are used.")
