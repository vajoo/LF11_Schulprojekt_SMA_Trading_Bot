import numpy as np
import yfinance as yf

class GenerateHistoricalDataframeForStock():
    def __init__(self, symbol):
        self.symbol = symbol
        self.dataframe = None
        self.__create_dataframe_with_historical_prices_for_symbol()
        self.__reset_dataframe_index()
        self.__convert_dataframe_datetime_column_to_european_timezone()
        self.__append_stock_returns_to_dataframe()

    def get_dataframe(self):
        return self.dataframe

    def __create_dataframe_with_historical_prices_for_symbol(self):
        self.dataframe = yf.download(self.symbol, interval='1m', period='7d', rounding=True)
    
    def __reset_dataframe_index(self):
        self.dataframe = self.dataframe['Close'].reset_index()
        
    def __convert_dataframe_datetime_column_to_european_timezone(self):
        self.dataframe['Datetime'] = self.dataframe['Datetime'].dt.tz_convert('Europe/Berlin').dt.tz_localize(None)
    
    def __append_stock_returns_to_dataframe(self):
        self.dataframe["returns"] = np.log(self.dataframe["Close"].div(self.dataframe["Close"].shift(1)))