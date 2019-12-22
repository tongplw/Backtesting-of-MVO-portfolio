import pandas as pd
import matplotlib.pyplot as plt
import optimizer as opt
from datetime import datetime


stocks = ['PTT', 'CPALL', 'SCC', 'BDMS', 'AOT']
MONEY = 1000000
reallocate = 1  # month:0, year:1

def plot_stocks():
    df = opt.getStockDataFrame(stocks)
    volume = {name: 0 for name in stocks}
    weight = {name: 0 for name in stocks}

    money = MONEY
    tem = 0

    plt_day = []
    plt_val = []

    for index, row in enumerate(df.iterrows()):
        date = row[0]
        price = row[1]

        # calculate every month or every year
        routine = date.month if reallocate else date.day
        if routine < tem:

            # calculate total money by selling all
            for stock in stocks:
                money += volume[stock] * price[stock]

            weight = opt.allocate(df.iloc[:index])
            
            # calculate new volume
            for stock in stocks:
                available = weight[stock] * money
                volume[stock] = available // price[stock]
                money -= volume[stock] * price[stock]
        
        plt_day += [date]
        plt_val += [money + sum(volume[stock] * price[stock] for stock in stocks)]
        tem = routine
    plt.plot(plt_day, plt_val)


def plot_set_index():
    money = MONEY
    volume = 0
    plt_day = []
    plt_val = []
    data = pd.read_csv("SET50.csv", index_col=0)
    for date, price in data.iterrows():
        plt_day += [datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')]

        if money >= price['Close']:
            volume = money / price['Close']
            money = 0
        
        # if money >= price['Close']:
        #     volume += money // price['Close']
        #     money %= price['Close']

        plt_val += [volume * price['Close']]

    plt.plot(plt_day, plt_val)

plot_stocks()
plot_set_index()
plt.show()