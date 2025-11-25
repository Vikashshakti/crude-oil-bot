import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pandas_ta as ta
import requests
BOT_TOKEN = "8333571482:AAFyQZfJOTQpmPDsffSaPlEAbExOLnJB7Ms"
CHAT_ID = "5343445157"
def fetch_stock_data(ticker, period='1d', interval='1m'):
    """
    Fetch current stock data for a given ticker symbol.

    
    Parameters:
    ticker (str): The stock ticker symbol.
    period (str): The period over which to fetch data (default is '1mo').
    interval (str): The data interval (default is '1d').

    Returns:
    pd.DataFrame: DataFrame containing the historical stock data.
    """

    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist
def calculate_technical_indicators(df):
    """ Calculate technical indicators for the stock data.  
    Parameters:
    df (pd.DataFrame): DataFrame containing stock data with 'Close' prices.
    Returns:
    pd.DataFrame: DataFrame with added technical indicators.
    """
    df['SMA_14'] = ta.sma(df['Close'], length=14)
    df['EMA_14'] = ta.ema(df['Close'], length=14)
    df['RSI_14'] = ta.rsi(df['Close'], length=14)
    return df

if not BOT_TOKEN or not CHAT_ID:
    print("Error: Missing environment variables (BOT_TOKEN or CHAT_ID).")
    

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Failed to send message: {e}")

def check_market():
    print(f"Fetching data for Crude Oil...")
    
    df = fetch_stock_data('MCL=F', period='1d', interval='5m')
    df = calculate_technical_indicators(df)
    SYMBOL = 'MCL=F'
    INTERVAL = '5m'
    RSI_PERIOD = 14
    if df is None or df.empty:
        print("No data received.")
        return

    current_rsi = df['RSI_14'].iloc[-1]
    prev_rsi = df['RSI_14'].iloc[-2]
    current_price = df['Close'].iloc[-1]

    print(f"Analyzed {SYMBOL}: Prev RSI={prev_rsi:.2f}, Curr RSI={current_rsi:.2f}")

    # LOGIC 1: RSI Recovery (Crossing UP above 30)
    if prev_rsi <= 30 and current_rsi > 30:
        msg = f"🛢 **OIL ALERT (12Data): BUY**\n\n{SYMBOL} ({INTERVAL}) RSI crossed ABOVE 30.\n**RSI:** {current_rsi:.2f}\n**Price:** ${current_price:.2f}"
        send_telegram_message(msg)
        print("Buy Alert Sent")

    # LOGIC 2: RSI Cooldown (Crossing DOWN below 80)
    elif prev_rsi >= 80 and current_rsi < 80:
        msg = f"🔥 **OIL ALERT (12Data): SELL**\n\n{SYMBOL} ({INTERVAL}) RSI crossed BELOW 80.\n**RSI:** {current_rsi:.2f}\n**Price:** ${current_price:.2f}"
        send_telegram_message(msg)
        print("Sell Alert Sent")
    
    else:
        print("No crossover detected.")

 if __name__ == "__main__":
     check_market()

