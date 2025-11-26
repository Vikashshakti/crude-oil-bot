#Importing Libraries
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pandas_ta as ta
import requests


# Telegram Bot Tokens
BOT_TOKEN = "8350301832:AAFLj6xSI4caABwQEHOjbl2bxOEF6rPwlMY"
CHAT_ID = "7994825155"

# Fetching Function Stock data from yahoo finance
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
    df['RSI_14'] = ta.rsi(df['Close'], length=14) # Change RSI timeframe.
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
    SYMBOL = 'MCL=F'  # Crude Oil Symbol , Symbo, Change here 
    INTERVAL = '5m'   # Interval  Change here 
    df = fetch_stock_data(SYMBOL, period='1d', interval=INTERVAL) # Storing the historical data into df
    df = calculate_technical_indicators(df) # Applying TI on the data and storing under same name i.e. df

    if df is None or df.empty:
        print("No data received.")
        return

    current_rsi = df['RSI_14'].iloc[-1]  # Last row of data 
    prev_rsi = df['RSI_14'].iloc[-2]   # Second Last row
    current_price = df['Close'].iloc[-1] # Last row of Price 

    print(f"Analyzed {SYMBOL}: Prev RSI={prev_rsi:.2f}, Curr RSI={current_rsi:.2f}")
    low_rsi= 30 
    high_rsi = 80 
    # LOGIC 1: RSI Recovery (Crossing UP above 30)
    if prev_rsi <= low_rsi and current_rsi > low_rsi:
        msg = f"🛢 **OIL ALERT (12Data): BUY**\n\n{SYMBOL} ({INTERVAL}) RSI crossed ABOVE {low_rsi}.\n**RSI:** {current_rsi:.2f}\n**Price:** ${current_price:.2f}"
        send_telegram_message(msg) # it will trigger this message to telegram 
        print("Buy Alert Sent")

    # LOGIC 2: RSI Cooldown (Crossing DOWN below 80)
    elif prev_rsi >= high_rsi and current_rsi < high_rsi:
        msg = f"🔥 **OIL ALERT (12Data): SELL**\n\n{SYMBOL} ({INTERVAL}) RSI crossed BELOW {high_rsi}.\n**RSI:** {current_rsi:.2f}\n**Price:** ${current_price:.2f}"
        send_telegram_message(msg)
        print("Sell Alert Sent")
    
    else:
        message =f"Analyzed {SYMBOL}: Prev RSI={prev_rsi:.2f}, Curr RSI={current_rsi:.2f}"
        send_telegram_message(message)
if __name__ == "__main__":
    check_market()






