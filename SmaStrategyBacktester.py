from scipy.optimize import brute

class SmaStrategyBacktester():
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.buy_prices_list = []
        self.sell_prices_list = []
        self.absolute_return = 0
        self.amount_of_trades = 0

    def get_optimal_sma_parameter(self, sma_s_range, sma_l_range):
        # for example (10, 51, 1), (100, 253, 1)
        optimal_sma_parameter = brute(self.run_sma_strategy, (sma_s_range, sma_l_range), finish=None)
        self.run_sma_strategy((optimal_sma_parameter[0], optimal_sma_parameter[1]))
        return (int(optimal_sma_parameter[0]), int(optimal_sma_parameter[1]))
    
    def run_sma_strategy(self, sma): 
        # for example (50, 100)
        self.__update_sma_columns_in_dataframe(sma)
        self.__set_buy_price_list_and_sell_price_list()
        self.absolute_return = self.__calculate_absolute_return_of_sma_strategy()
        self.amount_of_trades = self.__calculate_amount_of_trades()
        return -self.absolute_return

    def __update_sma_columns_in_dataframe(self, sma):
        if sma is not None:
            self.dataframe["SMA_S"] = self.dataframe["Close"].rolling(int(sma[0])).mean()
            self.dataframe["SMA_L"] = self.dataframe["Close"].rolling(int(sma[1])).mean()
    
    def __set_buy_price_list_and_sell_price_list(self):
        last_signal = "Sell"
        self.buy_prices_list = []
        self.sell_prices_list = []
        
        for i in range(len(self.dataframe["Close"])):
            if self.dataframe["SMA_S"][i] > self.dataframe["SMA_L"][i]:
                if last_signal != "Buy":
                    self.buy_prices_list.append(self.dataframe["Close"].iloc[i])
                    last_signal = "Buy"
            elif self.dataframe["SMA_L"][i] > self.dataframe["SMA_S"][i]:
                if last_signal != "Sell":
                    self.sell_prices_list.append(self.dataframe["Close"].iloc[i])
                    last_signal = "Sell"
                    
        self.__delete_last_element_from_buy_prices_list_if_last_signal_was_buy()

    def __delete_last_element_from_buy_prices_list_if_last_signal_was_buy(self):
        if len(self.buy_prices_list) != len(self.sell_prices_list):
            del self.buy_prices_list[-1]

    def __calculate_absolute_return_of_sma_strategy(self):
        abs_ret = 0
        for i in range(0, len(self.buy_prices_list)):
            abs_ret += self.sell_prices_list[i] - self.buy_prices_list[i]
        return abs_ret
    
    def __calculate_amount_of_trades(self):
        return len(self.buy_prices_list) * 2
    
    def get_absolute_return_of_sma_strategy(self):
        return round(self.absolute_return, 2)

    def get_amount_of_trades(self):
        return self.amount_of_trades