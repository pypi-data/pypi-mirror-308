import numpy as np
from scipy import stats

def calculate_statistics(stock_prices, market_prices):
    # Calculate the mean, median, mode, standard deviation, variance, covariance, and correlation
    mean = np.mean(stock_prices)
    median = np.median(stock_prices)
    
    # Corrected mode calculation
    mode_result = stats.mode(stock_prices)
    if isinstance(mode_result.mode, np.ndarray):
        mode = mode_result.mode[0]  # Access the mode value correctly
    else:
        mode = mode_result.mode  # If mode is a scalar, assign it directly
    
    std_dev = np.std(stock_prices)
    variance = np.var(stock_prices)
    
    # Calculate covariance and correlation between stock and market prices
    covariance = np.cov(stock_prices, market_prices)[0][1]
    correlation = np.corrcoef(stock_prices, market_prices)[0][1]
    
    # Prepare insights
    insights = {
        "Mean": mean,
        "Median": median,
        "Mode": mode,
        "Standard Deviation": std_dev,
        "Variance": variance,
        "Covariance": covariance,
        "Correlation Coefficient": correlation
    }
    
    return insights