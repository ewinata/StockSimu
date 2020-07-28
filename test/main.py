import yfinance as yf 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

ticker_list = ["SPY","TLT"]
# for ticker in ticker_list:
#     df = yf.download(ticker)
#     df.to_csv("{}.csv".format(ticker))

df = pd.DataFrame()

def breakline():
    print()
    print("######################")
    print()

score = 0
import random 
for x in range(0,11):
    spy = random.randint(0,101)/100
    spy = x/10
    tlt = 1 - spy
        
    ticker_dict = {"SPY":spy,
                    "TLT":tlt}
    for ticker in ticker_dict:
        df[ticker] = pd.read_csv("{}.csv".format(ticker),index_col = 0)["Close"]
        df["{} Delta%".format(ticker)] = df[ticker].pct_change() * 100
    df = df.dropna()


    df["Portfolio Delta%"] = 0
    for ticker in ticker_dict:
        df["Portfolio Delta%"] += (df["{} Delta%".format(ticker)]*ticker_dict[ticker])
    leverage = 1.5/df["Portfolio Delta%"].std()
    df["Portfolio Delta%"] *= leverage
    df["Portfolio"] = (df["Portfolio Delta%"]/100+1).cumprod()
    name = ""
    for ticker in ticker_dict:
        name += ticker + " : " + str(ticker_dict[ticker]) + " | "
    mean = df["Portfolio Delta%"].mean()
    risk = df["Portfolio Delta%"].std()
    sharpe = mean / risk

    if sharpe > score:
        max_cum = df["Portfolio"].iloc[-1]
        max_name = name
        max_mean = mean 
        max_risk = risk 
        max_sharpe = sharpe
        score = sharpe

    breakline()
    print(name)
    print("Cumulative :",df["Portfolio"].iloc[-1])
    print("Return :",mean)
    print("Risk :", risk)
    print("Sharpe :", sharpe)

    np.log(df["Portfolio"]).plot()
    plt.show()


breakline()
breakline()
print(max_name)
print("Cumulative :",max_cum)
print("Return :",max_mean)
print("Risk :", max_risk)
print("Sharpe :", max_sharpe)