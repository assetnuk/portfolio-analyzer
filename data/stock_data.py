import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class StockDataCollector:
    def __init__(self):
        self.data = {}
    
    def get_stock(self, tickers, period='1y'):
        """Fetches stock data, stores in self.data"""
        # typecasting into a list because yf requires list input
        if isinstance(tickers, str):
            tickers = [tickers]
        
        stock_data = yf.download(tickers, period=period)
        
        # storing the DataFrame into self.data
        if len(tickers) == 1:
            self.data[tickers[0]] = stock_data
        else:
            for ticker in tickers:
                ticker_data = stock_data.xs(ticker, level='Ticker', axis=1)
                ticker_data.columns = pd.MultiIndex.from_product([ticker_data.columns, [ticker]], names=['Price', 'Ticker'])
                
                self.data[ticker] = ticker_data
        
        return stock_data
    
    def get_returns(self, ticker):
        """Calculates returns by date, raises ValueError if ticker not found in portfolio"""
        if ticker not in self.data:
            raise ValueError(f"No data for {ticker}")
        
        # auto_adjust True by default, so Close is already adjusted
        prices = self.data[ticker]['Close']
        returns = prices.pct_change().dropna()
        return returns

if __name__ == "__main__":
    collector = StockDataCollector()
    
    # test get_stock, Target Corp. as the default stock to display
    data = collector.get_stock('TGT')
    print('Testing stock fetching:\n')
    print('Rows, columns:', data.shape, '\n')
    print('Last 5 dates:\n', data.tail())
    
    # test get_returns
    returns = collector.get_returns('TGT')
    print('\n\nTesting returns:\n')
    print('Rows, columns:', returns.shape, '\n')
    print('Last 5 dates:\n', returns.tail())
