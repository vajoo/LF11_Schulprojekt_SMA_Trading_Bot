import sqlite3

db_file = "trading_bot.db"

def store_optimal_sma_parameter_to_db(symbol, optimal_parameter, absolute_return, amount_of_trades):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sma_optimal_parameter (Symbol TEXT, Optimal_Parameter TEXT, Absolute_Return REAL, Amount_Of_Trades INT, Last_Signal TEXT)")
    if get_optimal_sma_parameter_from_db(symbol) == None:
        cur.execute("INSERT INTO sma_optimal_parameter (Symbol, Optimal_Parameter, Absolute_Return, Amount_Of_Trades, Last_Signal) VALUES (?, ?, ?, ?, ?)", (symbol, str(optimal_parameter), absolute_return, amount_of_trades, "Sell"))
    else:
        cur.execute("UPDATE sma_optimal_parameter SET Optimal_Parameter = ?, Absolute_Return = ?, Amount_Of_Trades = ? WHERE Symbol = ?", (str(optimal_parameter), absolute_return, amount_of_trades, symbol))
    conn.commit()
    conn.close()

def get_optimal_sma_parameter_from_db(symbol):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT Optimal_Parameter FROM sma_optimal_parameter WHERE Symbol = ?", (symbol,))
    opt_param = cur.fetchone()
    conn.commit()
    conn.close()
    if opt_param != None:
        return eval(opt_param[0])
    
def set_last_signal(symbol, new_last_signal):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("UPDATE sma_optimal_parameter SET Last_Signal = ? WHERE Symbol = ?", (new_last_signal, symbol))
    conn.commit()
    conn.close()

def get_last_signal(symbol):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT Last_Signal FROM sma_optimal_parameter WHERE Symbol = ?", (symbol,))
    signal = cur.fetchone()
    conn.commit()
    conn.close()
    return signal
    
def clear_table():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM sma_optimal_parameter WHERE 1=1")
    conn.commit()
    conn.close()

def drop_table():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DROP TABLE sma_optimal_parameter")
    conn.commit()
    conn.close()