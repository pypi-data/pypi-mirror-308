import pandas as pd
import matplotlib.pyplot as plt

def calculate_rsi(prices, period=14):
    # Convert prices to a Pandas Series
    prices = pd.Series(prices)
    delta = prices.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def plot_rsi(prices):
    rsi = calculate_rsi(prices)
    plt.figure(figsize=(10, 6))
    plt.plot(rsi, label="RSI")
    plt.axhline(30, color='red', linestyle='--', label='Oversold (30)')
    plt.axhline(70, color='green', linestyle='--', label='Overbought (70)')
    plt.legend()
    plt.title("RSI Plot")
    plt.show()

    if rsi.iloc[-1] < 30:
        return "BUY"
    elif rsi.iloc[-1] > 70:
        return "SELL"
    else:
        return "HOLD"
