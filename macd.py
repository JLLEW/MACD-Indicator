def ema(n, sample_set):
    alfa = 2/(n+1)
    up = sum(map(lambda x,y: x*(1-alfa)**y, sample_set, range(n)))
    down = sum(map(lambda x: (1-alfa)**x, range(n)))
    result = up/down
    return result

def macd(n, sample_set):
    result = []
    samples = list(reversed(sample_set))
    for i in range(n):
        result.append(ema(12, samples[i:12+i]) - ema(26, samples[i:26+i]))
    return list(reversed(result))

def signal(n, sample_set):
    result = []
    samples = list(reversed(sample_set))
    for i in range(n):
        result.append(ema(9, samples[i:9+i]))
    return list(reversed(result))

import pandas as pd
#wig20 stands for capitalization-weighted stock market index of the twenty largest companies on the Warsaw Stock Exchange.
df = pd.read_csv("wig20_d.csv")
#calculating macd and signal for imported samples
samples = list(df.Zamkniecie)
macd_vec = macd(1000, samples)
signal_vec = signal(1000, macd_vec)
value = samples[-1000:]

#plotting calculated data
import matplotlib.pyplot as plt
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")
plt.plot(value, label="price", color="green")
plt.rcParams['figure.figsize'] = 10, 5
plt.title("WIG20")
plt.grid(True)
plt.legend()
plt.show()

plt.plot(macd_vec, label="MACD")
plt.plot(signal_vec, label="SIGNAL")
plt.rcParams['figure.figsize'] = 10, 5
plt.title("MACD/SIGNAL")
plt.grid(True)
plt.legend()
plt.show()

import random


#basic buying/selling simulation algorithm
#it checks if macd/signal lines crossed and according to position of lines takes decision about buying or selling
def simulation(data_set, money, simul_time, plot=""):
    start_money = money
    stocks = 0.0
    macd_list = macd(simul_time, data_set)
    signal_list = signal(simul_time, macd_list)
    value_list = list(reversed(data_set)) #date order in data_set is descending, starting from recent date
    buy_signals = []
    sell_signals = []
    for day in range(1, simul_time-1):
        sell = macd_list[day] > signal_list[day]
        buy = macd_list[day] < signal_list[day]
        sell_cross = macd_list[day-1] < signal_list[day-1]
        buy_cross = macd_list[day-1] > signal_list[day-1]
        crossed = (buy and buy_cross) or (sell and sell_cross)
    
        if buy and crossed and value_list[day] > 0 and money>0:
            ammount = money
            stocks += ammount/value_list[day]
            money -= ammount
            buy_signals.append(day)
            
        elif sell and crossed and value_list[day] > 0 and stocks>0:
            ammount = stocks
            stocks -= ammount
            money += ammount*value_list[day]
            sell_signals.append(day)
            
    money += stocks*value_list[simul_time - 1]
    profit = money/start_money*100.0 -100.0
    if plot == "print_plot":
        print("starting ammount: " + str(start_money) + " current ammount: " + str(money) + " profit " + str(profit) + "%")
        plt.plot(macd_list, '-ro', markevery=sell_signals, label="MACD")
        plt.plot(signal_list, '-b*', markevery=buy_signals, label="SIGNAL")
        plt.rcParams['figure.figsize'] = 10, 5
        plt.title("SIMUL CHART")
        plt.grid(True)
        plt.legend()
        plt.show()
    elif plot == "print_summary":
        print("profit: "+ str(profit))
    return profit
        
simulation(samples, 10000, 1000, "print_plot")
sim_list = list(map(lambda x: simulation(samples, 10000, x, "print_summary"), range(100,1300,100)))
print("avg profit: " + str(sum(sim_list)/len(sim_list)))
        
