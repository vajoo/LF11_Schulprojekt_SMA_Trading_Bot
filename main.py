from GenerateHistoricalDataframeForStockprices import *
from SmaStrategyBacktester import *

msft_dataframe = GenerateHistoricalDataframeForStockprices("MSFT")
# print(msft_dataframe.get_dataframe())

msft_backtester = SmaStrategyBacktester(msft_dataframe.get_dataframe())
msft_backtester.run_sma_strategy((50, 113))
print("Absolute return: " + str(msft_backtester.get_absolute_return_of_sma_strategy()))
print("Amount of trades: " + str(msft_backtester.get_amount_of_trades()))
optimal_parameter = msft_backtester.get_optimal_sma_parameter((10, 51, 1), (100, 251, 1))
print(optimal_parameter)
# print(msft_backtester.dataframe)
print("Absolute return: " + str(msft_backtester.get_absolute_return_of_sma_strategy()))
print("Amount of trades: " + str(msft_backtester.get_amount_of_trades()))