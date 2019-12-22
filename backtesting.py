import pandas as pd
import optimizer as opt
from datetime import datetime
import matplotlib.pyplot as plt


stocks = ['PTT', 'CPALL', 'SCC', 'BDMS', 'AOT']
MONEY = 1000000
FEE = 0.0015

# import and clean data
df = opt.getStockDataFrame(stocks)
df.at[datetime.strptime('1/2/2009', '%m/%d/%Y'), 'PTT'] = 17.5
df.at[datetime.strptime('7/6/2009', '%m/%d/%Y'), 'PTT'] = 22.7


def plot_monthly_with_fee():
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
        routine = date.day
        if routine < tem:

            # calculate total money by selling all
            for stock in stocks:
                money += volume[stock] * price[stock]

            weight = opt.allocate(df.iloc[:index])
            
            # calculate new volume
            for stock in stocks:
                available = weight[stock] * money
                volume[stock] = (available * (1 - FEE)) / price[stock]
                money -= available
        
        plt_day += [date]
        plt_val += [money + sum(volume[stock] * price[stock] for stock in stocks)]
        tem = routine
    plt.plot(plt_day, plt_val, label='monthly with fee')


def plot_monthly_without_fee():
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
        routine = date.day
        if routine < tem:

            # calculate total money by selling all
            for stock in stocks:
                money += volume[stock] * price[stock]

            weight = opt.allocate(df.iloc[:index])
            
            # calculate new volume
            for stock in stocks:
                available = weight[stock] * money
                volume[stock] = available / price[stock]
                money -= available
        
        plt_day += [date]
        plt_val += [money + sum(volume[stock] * price[stock] for stock in stocks)]
        tem = routine
    plt.plot(plt_day, plt_val, label='monthly without fee')


def plot_annually_with_fee():
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
        routine = date.month
        if routine < tem:

            # calculate total money by selling all
            for stock in stocks:
                money += volume[stock] * price[stock]

            weight = opt.allocate(df.iloc[:index])
            
            # calculate new volume
            for stock in stocks:
                available = weight[stock] * money
                volume[stock] = (available * (1 - FEE)) / price[stock]
                money -= available
        
        plt_day += [date]
        plt_val += [money + sum(volume[stock] * price[stock] for stock in stocks)]
        tem = routine
    plt.plot(plt_day, plt_val, label='yearly with fee')


def plot_annually_without_fee():
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
        routine = date.month
        if routine < tem:

            # calculate total money by selling all
            for stock in stocks:
                money += volume[stock] * price[stock]

            weight = opt.allocate(df.iloc[:index])
            
            # calculate new volume
            for stock in stocks:
                available = weight[stock] * money
                volume[stock] = available / price[stock]
                money -= available
        
        plt_day += [date]
        plt_val += [money + sum(volume[stock] * price[stock] for stock in stocks)]
        tem = routine
    plt.plot(plt_day, plt_val, label='yearly without fee')


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

        plt_val += [volume * price['Close']]

    plt.plot(plt_day, plt_val, label='SET50')
    

plot_monthly_with_fee()
plot_monthly_without_fee()
plot_annually_with_fee()
plot_annually_without_fee()
plot_set_index()

plt.legend(bbox_to_anchor=(0.7, 0.3), loc='upper left', borderaxespad=0.)
plt.show()