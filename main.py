import yfinance as yf

def get_1m_historical_data(ticker):
    interval = '1m'
    period = '7d'
    hist_data = yf.download(ticker, interval=interval, period=period, rounding=True)
    hist_data = hist_data['Close'].reset_index()
    hist_data['Datetime'] = hist_data['Datetime'].dt.tz_convert('Europe/Berlin').dt.tz_localize(None)
    return hist_data

print(get_1m_historical_data("MSFT"))