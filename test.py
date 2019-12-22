import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


plt_day = []
plt_val = []

data = pd.read_csv("monthly.csv", index_col=0)
for index, row in enumerate(data.iterrows()):
    plt_day += [datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S')]
    plt_val += [row[1]['Close']]

plt.plot(plt_day, plt_val)
plt.show()