import pandas as pd
import matplotlib.pyplot as plt

def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    prices = pd.Series(prices)
    short_ema = prices.ewm(span=short_period, adjust=False).mean()
    long_ema = prices.ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal

def plot_macd(prices):
    macd, signal = calculate_macd(prices)
    plt.figure(figsize=(10, 6))
    plt.plot(macd, label="MACD", color='blue')
    plt.plot(signal, label="Signal Line", color='red')
    plt.legend()
    plt.title("MACD Plot")
    plt.show()

    if macd.iloc[-1] > signal.iloc[-1]:
        return "BUY"
    elif macd.iloc[-1] < signal.iloc[-1]:
        return "SELL"
    else:
        return "HOLD"
