
import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# Define default output path
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
os.makedirs(DATA_DIR, exist_ok=True)

# Example list of tickers: Stocks, Crypto, Commodities (USA, EU, Norway, Switzerland)
DEFAULT_TICKERS = [
    'AAPL',         # Apple (USA)
    'NESN.SW',      # Nestlé (Switzerland)
    'EQNR.OL',      # Equinor (Norway)
    'SAP.DE',       # SAP (Germany)
    'BTC-USD',      # Bitcoin
    'ETH-USD',      # Ethereum
    'GC=F',         # Gold Futures
    'CL=F'          # Crude Oil Futures
]

def download_prices(tickers=DEFAULT_TICKERS, start='2018-01-01', end=None):
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')

    print(f"Downloading data from {start} to {end} for {len(tickers)} tickers...")

    for ticker in tickers:
        try:
            print(f"  → {ticker}")
            df = yf.download(ticker, start=start, end=end)
            if df.empty:
                print(f"    ⚠️ No data for {ticker}")
                continue
            df = df[['Close']].rename(columns={'Close': ticker})
            df.to_csv(os.path.join(DATA_DIR, f"{ticker}.csv"))
        except Exception as e:
            print(f"    ❌ Error downloading {ticker}: {e}")

if __name__ == "__main__":
    download_prices()
