# ATACS (Automated Technical Analysis Calculation and Suggestions)

ATACS is a Python package designed for stock market analysis. It provides functionality to:
- Calculate and visualize key technical indicators like **RSI** (Relative Strength Index) and **MACD** (Moving Average Convergence Divergence).
- Perform statistical analysis on stock prices, including calculating central tendency measures like mean, median, mode, and measures of dispersion like standard deviation, variance, covariance, and correlation.

This package is useful for traders, analysts, and financial data scientists who want to quickly assess technical indicators and market trends for decision-making.

## Features

- **RSI Calculation and Visualization**: Calculates the Relative Strength Index and visualizes it alongside stock prices, suggesting "Buy," "Hold," or "Sell" based on predefined thresholds.
- **MACD Calculation and Visualization**: Calculates and plots the Moving Average Convergence Divergence, with buy/sell/hold recommendations.
- **Statistical Analysis**: Calculate central tendency measures (mean, median, mode), dispersion (standard deviation, variance), and correlation analysis between stock prices and market indices.

## Installation

To install the `ATACS` package, you can use `pip`:

```bash
pip install atacs
```

## Usage

Here's an example of how to use the package:

RSI Calculation and Visualization:

from atacs.rsi import calculate_rsi, plot_rsi

stock_prices = [120, 122, 123, 124, 122, 121, 120, 119, 118, 119]
rsi = calculate_rsi(stock_prices)
plot_rsi(stock_prices)

MACD Calculation and Visualization:

from atacs.macd import calculate_macd, plot_macd

stock_prices = [120, 122, 123, 124, 122, 121, 120, 119, 118, 119]
macd = calculate_macd(stock_prices)
plot_macd(stock_prices)

Statistical Analysis:

from atacs.stats import calculate_statistics

stock_prices = [120, 122, 123, 124, 122, 121, 120, 119, 118, 119]
market_index = [2000, 2020, 2030, 2050, 2020, 2005, 1995, 1980, 1970, 1985]
statistics = calculate_statistics(stock_prices, market_index)
print(statistics)

License
MIT License. See the LICENSE file for more information.