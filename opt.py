import datetime
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from scipy import optimize


def getStockDataFrame(stocks):
    """Return data frame of daily stock's price"""
    stocks = [stock.strip()+'.BK' for stock in stocks]
    w = pd.DataFrame()
    t = []
    for s in stocks:
        data = pdr.get_data_yahoo(
            s, 
            start=datetime.datetime(2009, 1, 1), 
            end=datetime.datetime(2019, 1, 1),
            interval='d'
        )
        px = data[['Close']]
        t.append(px)
    w = pd.concat(t, axis=1, join='outer')
    w.columns = [name.split('.')[0] for name in stocks]
    return w

def allocate(stocks_dataframe):
    portfolio_size = len(stocks_dataframe.columns)
    returns = stocks_dataframe.pct_change()
    mean_return = np.array(returns.mean())
    annualized_return = np.round(mean_return * 252.0, 2)
    cov_matrix = np.multiply(returns.cov(), 252.0)

    def portfolio_return(x):
        return np.array(np.dot(x.T, annualized_return))

    def portfolio_var(x):
        return np.array((np.dot(np.dot(x.T, cov_matrix), x)))

    def target(x):
        return np.array(-1 * (0.1 * portfolio_return(x) - portfolio_var(x)))

    # Optimize
    initial_guess = np.random.random(portfolio_size)
    initial_guess = initial_guess / sum(initial_guess)
    out = optimize.minimize(target, initial_guess, bounds=tuple([(0.05, 1)] * portfolio_size))
    out.x = out.x / np.sum(np.abs(out.x))

    weights = {}
    for i in range(portfolio_size):
        weights[stocks_dataframe.columns[i]] = out.x[i]

    return weights