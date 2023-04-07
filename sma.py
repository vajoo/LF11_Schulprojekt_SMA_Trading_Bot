import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import brute

class SMA():

    def __init__(self, symbol, sma=(50, 100)):
        self.symbol = symbol
        self.sma = sma
        self.amount_of_trades = 0
        self.buy_price = []
        self.sell_price = []
        self.absolute_return = 0
        self.dataframe = self.create_dataframe_with_historical_prices_for_symbol()
        self.reset_dataframe_index()
        self.convert_dataframe_datetime_column_to_european_timezone()
        self.set_sma_columns()
        self.append_returns_to_dataframe()

    def create_dataframe_with_historical_prices_for_symbol(self):
        return self.get_1m_historical_price_data()

    def get_1m_historical_price_data(self):
        return yf.download(self.symbol, interval='1m', period='7d', rounding=True)
    
    def reset_dataframe_index(self):
        self.dataframe = self.dataframe['Close'].reset_index()
        
    def convert_dataframe_datetime_column_to_european_timezone(self):
        self.dataframe['Datetime'] = self.dataframe['Datetime'].dt.tz_convert('Europe/Berlin').dt.tz_localize(None)
    
    def append_returns_to_dataframe(self):
        self.dataframe["returns"] = np.log(self.dataframe["Close"].div(self.dataframe["Close"].shift(1)))

    def optimize_parameters(self, sma_s_range, sma_l_range):
        # (10, 51, 1), (100, 253, 1)
        optimal_sma_parameter = brute(self.run_sma_strategy, (sma_s_range, sma_l_range), finish=None)
        self.set_sma_parameter((optimal_sma_parameter[0], optimal_sma_parameter[1]))
    
    def run_sma_strategy(self, sma):
        self.set_sma_parameter(sma)
        self.set_sma_columns()
        self.set_buy_price_list_and_sell_price_list()
        self.delete_last_element_from_buy_price_element_if_buy_signal_was_last_action()
        self.calculate_absolute_return_of_sma_strategy()
        return -self.get_absolute_return_of_sma_strategy()
    
    def set_sma_parameter(self, sma):
        self.sma = (int(sma[0]), int(sma[1]))

    def set_sma_columns(self):
        self.dataframe["SMA_S"] = self.dataframe["Close"].rolling(self.sma[0]).mean()
        self.dataframe["SMA_L"] = self.dataframe["Close"].rolling(self.sma[1]).mean()

    def get_absolute_return_of_sma_strategy(self):
        return round(self.absolute_return, 2)
    
    def set_buy_price_list_and_sell_price_list(self):
        signal = -1
        self.buy_price = []
        self.sell_price = []
        
        for i in range(len(self.dataframe["Close"])):
            if self.dataframe["SMA_S"][i] > self.dataframe["SMA_L"][i]:
                if signal != 1:
                    self.buy_price.append(self.dataframe["Close"].iloc[i])
                    signal = 1
            elif self.dataframe["SMA_L"][i] > self.dataframe["SMA_S"][i]:
                if signal != -1:
                    self.sell_price.append(self.dataframe["Close"].iloc[i])
                    signal = -1

    def delete_last_element_from_buy_price_element_if_buy_signal_was_last_action(self):
        if len(self.buy_price) != len(self.sell_price):
            del self.buy_price[-1]

    def calculate_absolute_return_of_sma_strategy(self):
        abs_ret = 0
        for i in range(0, len(self.buy_price)):
            abs_ret += self.sell_price[i] - self.buy_price[i]
        self.absolute_return = abs_ret

    def get_amount_of_trades(self):
        return len(self.buy_price)
    
    def set_amount_of_trades(self):
        self.amount_of_trades = len(self.buy_price)
    

    
msft = SMA("MSFT")
msft.run_sma_strategy(msft.sma)
print(msft.get_absolute_return_of_sma_strategy())
print(msft.dataframe)


msft.optimize_parameters((10, 51, 1), (100, 253, 1))
msft.run_sma_strategy(msft.sma)
print(msft.sma)
print(msft.get_absolute_return_of_sma_strategy())
print(msft.dataframe)