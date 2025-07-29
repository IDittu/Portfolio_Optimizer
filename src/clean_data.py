
import pandas as pd
import os

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def load_and_clean_data():
    price_dfs = []
    tickers = []

    for filename in os.listdir(RAW_DATA_DIR):
        if filename.endswith('.csv'):
            ticker = filename.replace('.csv', '')
            try:
                df = pd.read_csv(os.path.join(RAW_DATA_DIR, filename), index_col='Date', parse_dates=True)
                df = df[[ticker]] if ticker in df.columns else df.rename(columns={df.columns[0]: ticker})
                price_dfs.append(df)
                tickers.append(ticker)
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")

    if not price_dfs:
        print("⚠️ No valid CSV files found.")
        return None

    # Combine and clean
    combined = pd.concat(price_dfs, axis=1)
    combined = combined.sort_index()
    combined = combined.dropna(how='any')  # Drop rows with any missing values

    # Save cleaned data
    output_path = os.path.join(PROCESSED_DATA_DIR, 'merged_prices.csv')
    combined.to_csv(output_path)
    print(f"✅ Cleaned data saved to {output_path}")

    return combined

if __name__ == "__main__":
    load_and_clean_data()
