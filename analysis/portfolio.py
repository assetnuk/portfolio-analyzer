import pandas as pd
import numpy as np
from data.stock_data import StockDataCollector

class Portfolio:
    def __init__(self, tickers, weights=None):
        self.tickers = tickers
        self.weights = weights or [1/len(tickers)] * len(tickers)
        self.collector = StockDataCollector()
        self.returns = None
        self.portfolio_returns = None
        
    def get_data(self, period='1y'):
        """Loads data for all stocks in the portfolio"""
        data = self.collector.get_stock(self.tickers, period)
        
        # stores the returns for individual stocks in the portfolio
        returns_list = []
        for ticker in self.tickers:
            returns_df = self.collector.get_returns(ticker)  
            returns_list.append(returns_df)

        self.returns = pd.concat(returns_list, axis=1)
        
        
    def get_metrics(self):
        """Calculates metrics for portfolio analysis: Returns, Risk, Sharpe, Sortino, Maximum Drawdown"""
        if self.returns is None:
            raise ValueError("No data loaded")
        
        # full portfolio returns calculation, weighted avg
        self.portfolio_returns = (self.returns * self.weights).sum(axis=1)
        
        # a simple actual trading days calculation for more accuracy
        trading_days = len(self.portfolio_returns)
        years_of_data = (self.portfolio_returns.index[-1] - self.portfolio_returns.index[0]).days / 365.25
        trading_days_per_year = trading_days / years_of_data
        
        # 10-year treasury bond rate as of July 2025
        risk_free_rate = 0.0435
        
        # returns and risk
        daily_return = self.portfolio_returns.mean()
        daily_volatility = self.portfolio_returns.std()
        annual_return = daily_return * trading_days_per_year
        annual_volatility = daily_volatility * np.sqrt(trading_days_per_year)
        
        # risk-adjusted returns of the portfolio using Sharpe ratio
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
        
        # downside risk-adjusted returns using Sortino ratio
        negative_returns = self.portfolio_returns[self.portfolio_returns < 0]
        downside_risk = negative_returns.std() * np.sqrt(trading_days_per_year)
        sortino_ratio = (annual_return - risk_free_rate) / downside_risk
        
        # max drawdown to see maximum possible downside
        cumulative_returns = (1 + self.portfolio_returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdowns = (cumulative_returns - rolling_max) / rolling_max
        max_drawdown = drawdowns.min()
        
        # return all metrics
        metrics = {
            'Daily Return': daily_return,
            'Daily Volatility': daily_volatility,
            'Annual Return': annual_return,
            'Annual Volatility': annual_volatility,
            'Sharpe Ratio': sharpe_ratio,
            'Sortino Ratio': sortino_ratio,
            'Maximum Drawdown': max_drawdown,
            'Trading Days Per Year': trading_days_per_year
        }
        
        return metrics
    
if __name__ == '__main__':
    # test for a sample portfolio, assume equal weights
    tickers = ['TGT', 'WMT', 'HD', 'AAPL', 'GOOGL', 'MSFT']
    
    portfolio = Portfolio(tickers)
    portfolio.get_data()
    
    metrics = portfolio.get_metrics()
    
    print("Portfolio Performance:")
    print("-" * 20)
    for key, value in metrics.items():
        if 'Ratio' in key or 'Return' in key or 'Volatility' in key or 'Drawdown' in key:
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value:.2f}")