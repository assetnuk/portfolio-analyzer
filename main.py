from analysis.portfolio import Portfolio
import sys

def print_header():
    """Print application header"""
    print("=" * 60)
    print("           Portfolio Risk & Performance Analyzer")
    print("=" * 60)
    print()

def get_portfolio_input():
    """Get portfolio composition from user"""
    print("Portfolio Setup:")
    print("-" * 20)
    
    # get tickers
    while True:
        tickers_input = input("Enter stock tickers (separated by commas): ").strip().upper()
        if tickers_input:
            tickers = [ticker.strip() for ticker in tickers_input.split(',')]
            break
        else:
            print("Please enter at least one ticker.")
    
    print(f"Tickers: {tickers}")
    
    # get weights
    while True:
        weights_choice = input(f"\nUse equal weights for all {len(tickers)} stocks? (y/n): ").strip().lower()
        
        if weights_choice in ['y', 'yes']:
            weights = None
            print("Using equal weights")
            break
        elif weights_choice in ['n', 'no']:
            print(f"Enter weights for {len(tickers)} stocks (must sum to 1.0):")
            weights = []
            total_weight = 0
            
            for ticker in tickers:
                while True:
                    try:
                        weight = float(input(f"Weight for {ticker}: "))
                        if 0 <= weight <= 1:
                            weights.append(weight)
                            total_weight += weight
                            break
                        else:
                            print("Weight must be between 0 and 1")
                    except ValueError:
                        print("Please enter a valid number")
            
            if abs(total_weight - 1.0) > 0.001:
                print(f"Weights sum to {total_weight:.3f}, should sum to 1.0")
                print("Using equal weights instead")
                weights = None
            break
        else:
            print("Please enter 'y' or 'n'")
    
    return tickers, weights

def get_time_period():
    """Get analysis time period from user"""
    print("\nTime Period:")
    print("-" * 20)
    
    periods = {
        '1': '3mo',
        '2': '6mo', 
        '3': '1y',
        '4': '2y',
        '5': '5y'
    }
    
    print("1. 3 months")
    print("2. 6 months") 
    print("3. 1 year (default)")
    print("4. 2 years")
    print("5. 5 years")
    
    while True:
        choice = input("Select time period (1-5): ").strip()
        if choice in periods:
            return periods[choice]
        elif choice == '':
            return '1y' 
        else:
            print("Please select a number between 1-5")

def format_metrics(metrics):
    """Format metrics for display""" 
    print("\nPortfolio Analysis Results:")
    print("=" * 50)
    
    # returns section
    print("\nRETURNS")
    print("-" * 30)
    print(f"Daily Return:       {metrics['Daily Return']:>8.4f} ({metrics['Daily Return']*100:>6.2f}%)")
    print(f"Annual Return:      {metrics['Annual Return']:>8.4f} ({metrics['Annual Return']*100:>6.2f}%)")
    
    # risk section  
    print(f"\nRISK")
    print("-" * 30)
    print(f"Daily Volatility:   {metrics['Daily Volatility']:>8.4f} ({metrics['Daily Volatility']*100:>6.2f}%)")
    print(f"Annual Volatility:  {metrics['Annual Volatility']:>8.4f} ({metrics['Annual Volatility']*100:>6.2f}%)")
    print(f"Maximum Drawdown:   {metrics['Maximum Drawdown']:>8.4f} ({metrics['Maximum Drawdown']*100:>6.2f}%)")
    
    # risk-adjusted returns
    print(f"\nRISK-ADJUSTED PERFORMANCE")
    print("-" * 30)
    print(f"Sharpe Ratio:       {metrics['Sharpe Ratio']:>8.4f}")
    print(f"Sortino Ratio:      {metrics['Sortino Ratio']:>8.4f}")
    
    # performance interpretation
    print(f"\nINTERPRETATION")
    print("-" * 30)
    
    sharpe = metrics['Sharpe Ratio']
    if sharpe > 1.0:
        sharpe_rating = "Excellent"
    elif sharpe > 0.5:
        sharpe_rating = "Good"  
    elif sharpe > 0:
        sharpe_rating = "Fair"
    else:
        sharpe_rating = "Poor"
    
    annual_vol = metrics['Annual Volatility']
    if annual_vol < 0.15:
        risk_level = "Low"
    elif annual_vol < 0.25:
        risk_level = "Moderate"
    else:
        risk_level = "High"
    
    print(f"Risk Level:         {risk_level}")
    print(f"Sharpe Rating:      {sharpe_rating}")
    print(f"Risk-Free Rate:     4.35% (10Y Treasury)")

def run_analysis():
    """Run complete portfolio analysis"""
    try:
        # get user inputs
        tickers, weights = get_portfolio_input()
        period = get_time_period()
        
        # create and analyze portfolio
        print(f"\nDownloading data for {len(tickers)} stocks...")
        portfolio = Portfolio(tickers, weights)
        portfolio.get_data(period)
        
        print("Calculating metrics...")
        metrics = portfolio.get_metrics()
        
        # display results
        format_metrics(metrics)
        
        return True
        
    except KeyboardInterrupt:
        print("\n\nAnalysis cancelled by user")
        return False
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        print("Please check your ticker symbols and try again.")
        return False

def main():
    """Main application"""
    print_header()
    
    while True:
        success = run_analysis()
        
        if not success:
            break
            
        print("\n" + "=" * 50)
        
        while True:
            continue_choice = input("\nAnalyze another portfolio? (y/n): ").strip().lower()
            if continue_choice in ['y', 'yes']:
                print("\n" + "=" * 60)
                break
            elif continue_choice in ['n', 'no']:
                print("\nThank you for using Portfolio Analyzer!")
                return
            else:
                print("Please enter 'y' or 'n'")

if __name__ == "__main__":
    main()