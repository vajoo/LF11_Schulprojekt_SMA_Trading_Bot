import yfinance as yf
import requests
from bs4 import BeautifulSoup
import datetime
import sqlite3

## to do: DB bauen, die sma parameter speichert

def get_1m_historical_price_data(ticker):
    interval = '1m'
    period = '7d'
    hist_data = yf.download(ticker, interval=interval, period=period, rounding=True)
    hist_data = hist_data['Close'].reset_index()
    hist_data["Signal"] = 0
    hist_data['Datetime'] = hist_data['Datetime'].dt.tz_convert('Europe/Berlin').dt.tz_localize(None)
    return hist_data

# def get_yahoo_finance_live_price_from_ticker(ticker): 
#     url = f"https://finance.yahoo.com/quote/{ticker}"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     price = soup.find("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text
#     return price

def store_historical_price_data_to_db(db_file, ticker, historical_price_data):
    conn = sqlite3.connect(db_file)
    historical_price_data.to_sql(ticker, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def safe_stock_price_into_db(db_file, ticker, price):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS stock_prices (Datetime DATE, Close REAL, Signal INT)")
    cur.execute("INSERT INTO stock_prices (Datetime, Close, Signal) VALUES (?, ?, ?)", (timestamp, float(price), 0))
    conn.commit()
    conn.close()

def clear_db(db_file, table_name):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM "+table_name+" WHERE 1=1")
    conn.commit()
    conn.close()

ticker = "MSFT"
data = get_1m_historical_price_data(ticker)
store_historical_price_data_to_db("ticker.db", ticker, data)