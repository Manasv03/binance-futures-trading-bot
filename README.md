# Binance Futures Trading Bot (Python)

A production-quality CLI-based Python trading bot that places Market and Limit orders on the Binance Futures Testnet (USDT-M) using direct REST API calls and HMAC-SHA256 signing.

## Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)
- A Binance Testnet account with API keys. Get them here: [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

## Setup Steps
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd trading_bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and fill in your Binance Testnet API Key and Secret:
     ```env
     BINANCE_API_KEY=your_testnet_api_key_here
     BINANCE_SECRET=your_testnet_secret_here
     ```

## How to Run
The bot supports both **MARKET** and **LIMIT** orders for USDT-margined pairs.

### Examples:

#### 1. Market BUY order
Place a market order to buy 0.001 BTC:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

#### 2. Limit SELL order
Place a limit order to sell 0.001 BTC at 80,000 USDT:
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 80000
```

#### 3. Validation Error Example
If you attempt a LIMIT order without a price, the bot will catch it:
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001
# Output: [ERROR] Validation Failed: Price is required for LIMIT orders.
```

## Project Structure
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client (auth, request signing, HTTP)
│   ├── orders.py          # Order placement logic (market, limit)
│   ├── validators.py      # Input validation (symbol, side, type, qty, price)
│   └── logging_config.py  # Logging setup (file + console handlers)
├── cli.py                 # CLI entry point using argparse
├── logs/                  # Log files directory (ignored by git except .gitkeep)
│   └── trading_bot.log    # Generated at runtime
├── .env.example           # Template for API keys
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
└── requirements.txt       # Project dependencies
```

## Assumptions Made
1. **Asset Precision**: This bot ignores asset precision (e.g., minimum quantity or price increments) as it depends on current exchange filters. Users must ensure provide valid quantities.
2. **Timezone**: All timestamps are generated locally in milliseconds which is compatible with Binance API as long as your system clock is synchronized.
3. **Connectivity**: Assumes a stable internet connection if running in a production-like environment.
