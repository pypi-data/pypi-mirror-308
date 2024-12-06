import numpy as np
import scipy.stats as stats

def calculate_statistics(stock_prices, market_prices):
    mean = np.mean(stock_prices)
    median = np.median(stock_prices)
    mode = stats.mode(stock_prices)[0][0]
    std_dev = np.std(stock_prices)
    variance = np.var(stock_prices)
    covariance = np.cov(stock_prices, market_prices)[0][1]
    correlation = np.corrcoef(stock_prices, market_prices)[0][1]

    insights = f"""
    Mean: {mean}
    Median: {median}
    Mode: {mode}
    Standard Deviation: {std_dev}
    Variance: {variance}
    Covariance with Market: {covariance}
    Correlation with Market: {correlation}
    """

    return insights
