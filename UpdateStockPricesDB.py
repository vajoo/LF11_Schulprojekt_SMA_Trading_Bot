import sqlite3
from GenerateHistoricalDataframeForStock import *
import pandas as pd

db_file = "trading_bot.db"
symbol = "MSFT"

def __get_dataframe():
    dataframe = GenerateHistoricalDataframeForStock(symbol).get_dataframe()[["Datetime", "Close"]]
    return dataframe

def store_historical_price_data_to_db():
    conn = sqlite3.connect(db_file)
    data = __get_dataframe()
    data.to_sql(symbol, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def get_historical_price_data_from_db():
    conn = sqlite3.connect(db_file)
    sql_query = pd.read_sql_query('SELECT * FROM {}'.format(symbol), conn)
    df = pd.DataFrame(sql_query, columns = ['Datetime', 'Close'])
    return df