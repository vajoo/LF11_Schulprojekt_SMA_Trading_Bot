import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import brute

class sma():

    def __init__(self, symbol, sma=(50, 100)):
        self.symbol = symbol
        self.sma = sma
        self.amount_of_trades = 0
        self.dataframe = self.create_dataframe()

    def create_dataframe(self):
        return self.append_sma_parameter_and_returns(self.get_1m_historical_price_data(self.symbol))

    def get_1m_historical_price_data(self, ticker):
        interval = '1m'
        period = '7d'
        hist_data = yf.download(ticker, interval=interval, period=period, rounding=True)
        hist_data = hist_data['Close'].reset_index()
        hist_data["Signal"] = 0
        hist_data['Datetime'] = hist_data['Datetime'].dt.tz_convert('Europe/Berlin').dt.tz_localize(None)
        return hist_data

    def append_sma_parameter_and_returns(self, df):
        df["SMA_S"] = df["Close"].rolling(self.sma[0]).mean()
        df["SMA_L"] = df["Close"].rolling(self.sma[1]).mean()
        df["returns"] = np.log(df["Close"].div(df["Close"].shift(1)))
        return df

    def set_parameters(self, sma = None):
        if sma is not None:
            self.sma = sma
            self.dataframe["SMA_S"] = self.dataframe["Close"].rolling(self.sma[0]).mean()
            self.dataframe["SMA_L"] = self.dataframe["Close"].rolling(self.sma[1]).mean()
    
    def implement_sma_strategy(self):
        data = self.dataframe
        sma_s = data["SMA_S"]
        sma_l = data["SMA_L"]
        close = data["Close"]
        buy_price = []
        sell_price = []
        sma_signal = []
        signal = -1
        
        for i in range(len(close)):
            if sma_s[i] > sma_l[i]:
                if signal != 1:
                    buy_price.append(close.iloc[i])
                    signal = 1
                    sma_signal.append(signal)
            elif sma_l[i] > sma_s[i]:
                if signal != -1:
                    sell_price.append(close.iloc[i])
                    signal = -1
                    sma_signal.append(-1)
                
        if len(buy_price) != len(sell_price):
            if(sma_signal[-1] == 1):
                del buy_price[-1]
                del sma_signal[-1]

        absolute_return = 0
        self.amount_of_trades = len(buy_price)

        for i in range(0, len(buy_price)):
            absolute_return += sell_price[i] - buy_price[i]

        return round(absolute_return, 2)
    
    def update_and_run(self, sma):
        self.set_parameters((int(sma[0]), int(sma[1])))
        return -self.implement_sma_strategy()

    def optimize_parameters(self, sma_s_range, sma_l_range):
        # (10, 50, 1), (100, 252, 1)
        opt = brute(self.update_and_run, (sma_s_range, sma_l_range), finish=None)
        return opt, -self.update_and_run(opt)