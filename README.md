# Portfolio Risk and Performance Analyzer
A python application for analyzing stock portfolio risk metrics and performance.

## Overview
This is a personal project to learn how to implement portfolio performance and risk analysis tools using `python`. Uses real-time market data and applies key models for insights.

### Key metrics
- **Portfolio returns:** Daily and Annualized returns
- **Risk metrics:** Volatility and Maximum Drawdown
- **Performance, risk-adjusted:** Sharpe and Sortino ratios
  
### Technicals
- **Real-time data:** Yahoo Finance integration through `yfinance`
- **Current risk-free rate:** Uses 10-year Treasury rate, 4.35%
- **Time periods:** 3mo, 6mo, 1y, 2y, 5y


## Output examples
### Input:
```
Enter stock tickers: nvda, googl, msft
Use equal weights for all 3 stocks? (y/n): y
Select time period (1-5): 2 (6 months)
```

### Output:
```
Portfolio Analysis Results:
==================================================

RETURNS
------------------------------
Daily Return:         0.0012 (  0.12%)
Annual Return:        0.3148 ( 31.48%)

RISK
------------------------------
Daily Volatility:     0.0231 (  2.31%)
Annual Volatility:    0.3677 ( 36.77%)
Maximum Drawdown:    -0.2680 (-26.80%)

RISK-ADJUSTED PERFORMANCE
------------------------------
Sharpe Ratio:         0.7378
Sortino Ratio:        1.0625

INTERPRETATION
------------------------------
Risk Level:         High
Sharpe Rating:      Good
Risk-Free Rate:     4.35% (10Y Treasury)

==================================================
```

## What I learned
- **Financial theory:** Sharpe and Sortino ratios, portfolio analysis tools
- **Data engineering:** Handling MultiIndex errors, extracting Series from DataFrame, combining DataFrames
- **Programming practices:** Error handling, structural architecture

## Future plans

### Verision 2:
- **Interactive visualization** using matplotlib/plotly charts
- **Portfolio optimization** recommendations with efficient frontier calculations
- **Benchmark comparisons**, alpha/beta vs S&P 500
- **Web interface** as a web-application

### Version 3:
- **Alternative securities:** commodities, bonds, etc.
- **Backtesting**
- **Machine Learning,** prediction models