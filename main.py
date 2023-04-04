import yfinance as yf
import requests
from bs4 import BeautifulSoup

def get_1m_historical_data(ticker):
    interval = '1m'
    period = '7d'
    hist_data = yf.download(ticker, interval=interval, period=period, rounding=True)
    hist_data = hist_data['Close'].reset_index()
    hist_data['Datetime'] = hist_data['Datetime'].dt.tz_convert('Europe/Berlin').dt.tz_localize(None)
    return hist_data

def get_yahoo_finance_live_price_from_ticker(ticker): 
    url = f"https://finance.yahoo.com/quote/{ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = soup.find("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text
    return price

print(get_yahoo_finance_live_price_from_ticker("AAPL"))
