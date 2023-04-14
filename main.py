from GenerateHistoricalDataframeForStock import *
from SmaStrategyBacktester import *
import UpdateStockPricesDB
import ProvideOptimalSMAParameter
import time
from datetime import datetime

symbol = "MSFT"

def backtest():
    UpdateStockPricesDB.store_historical_price_data_to_db()
    msft_backtester = SmaStrategyBacktester(UpdateStockPricesDB.get_historical_price_data_from_db())
    optimal_sma_parameter = msft_backtester.get_optimal_sma_parameter((10, 51, 1), (100, 251, 1))
    ProvideOptimalSMAParameter.store_optimal_sma_parameter_to_db("MSFT", optimal_sma_parameter, msft_backtester.get_absolute_return_of_sma_strategy(), msft_backtester.get_amount_of_trades())

def run_strategy():
    msft_backtester = SmaStrategyBacktester(UpdateStockPricesDB.get_historical_price_data_from_db())
    msft_backtester.run_sma_strategy(ProvideOptimalSMAParameter.get_optimal_sma_parameter_from_db(symbol))

def check_signal():
    df = UpdateStockPricesDB.get_historical_price_data_from_db()
    optimal_sma_parameter = ProvideOptimalSMAParameter.get_optimal_sma_parameter_from_db(symbol)
    df["SMA_S"] = df["Close"].rolling(int(optimal_sma_parameter[0])).mean()
    df["SMA_L"] = df["Close"].rolling(int(optimal_sma_parameter[1])).mean()
    if df.iloc[-1]["SMA_S"] > df.iloc[-1]["SMA_L"] and df.iloc[-2]["SMA_S"] < df.iloc[-2]["SMA_L"]:
        if ProvideOptimalSMAParameter.get_last_signal(symbol) == "Sell":
            print("Buy " + str(df.iloc[-1]["Close"]))
            ProvideOptimalSMAParameter.set_last_signal(symbol, "Buy")
    elif df.iloc[-1]["SMA_S"] < df.iloc[-1]["SMA_L"] and df.iloc[-2]["SMA_S"] > df.iloc[-2]["SMA_L"]:
        if ProvideOptimalSMAParameter.get_last_signal(symbol) == "Buy":
            print("Sell " + str(df.iloc[-1]["Close"]))
            ProvideOptimalSMAParameter.set_last_signal(symbol, "Sell")

if __name__ == "__main__":
    backtest()
    print("Backtest finished")
    while True:
        timestamp = int(time.time())
        hour_and_minute = int(datetime.now().strftime("%H%M"))
        if timestamp % 60 == 0 and hour_and_minute >= 1531 and hour_and_minute < 2200:
            UpdateStockPricesDB.store_historical_price_data_to_db()
            check_signal()
            time.sleep(1)

# TODO add column "Signal" to sma_optimal_parameter, check last column in prices db -> if buy then change signal to buy etc.