# Binance Futures Testnet Trading Bot

A Python CLI for placing Market and Limit orders on Binance Futures Testnet (USDT-M) using the `python-binance` library.

## Setup

1. Get API credentials from https://testnet.binancefuture.com/

2. Create `.env` file:
```
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Market Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Limit Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 150000
```

### Short Options
```bash
python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
python cli.py -s ETHUSDT -S SELL -t LIMIT -q 0.05 -p 3000
```

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance client wrapper (python-binance)
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── logs/                  # Log files
├── cli.py                 # CLI entry point
├── .env                   # API credentials
├── requirements.txt
└── README.md
```

## Features

- Market and Limit orders
- BUY and SELL support
- Input validation
- Logging to file and console
- Error handling

## Dependencies

- `python-binance` - Official Binance API wrapper
- `python-dotenv` - Environment variable management

## Assumptions

- Testnet only (https://testnet.binancefuture.com)
- USDT-M pairs only
- LIMIT orders use GTC (Good Till Cancelled)
