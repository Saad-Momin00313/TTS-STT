# AI-Powered Portfolio Management System

A comprehensive Python library for managing investment portfolios with AI-powered insights, financial analysis, and real-time tracking.

## Features

- Portfolio Management
- Financial Analysis
- AI Investment Advisor
- Finance Chatbot
- Real-time Asset Tracking
- Technical Analysis
- Risk Metrics
- Market Insights

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd portfolio-management
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your environment variables:

```bash
# Create .env file
GEMINI_API_KEY=your_gemini_api_key
```

## Usage Guide

### 1. Portfolio Management

```python
from src.portfolio_manager import PortfolioManager

# Initialize portfolio manager
portfolio = PortfolioManager()

# Add assets
asset_id = portfolio.add_asset(
    symbol="AAPL",
    asset_type="stock",
    quantity=10,
    purchase_price=150.0
)

# Get portfolio summary
summary = portfolio.get_portfolio_summary()
print(f"Total Portfolio Value: ${summary['total_portfolio_value']:,.2f}")
print(f"Total Gain/Loss: ${summary['total_gain_loss']:,.2f}")

# View risk metrics
risk_metrics = summary['risk_metrics']
print(f"Portfolio Volatility: {risk_metrics['volatility']:.2f}%")
print(f"Diversification Score: {risk_metrics['diversification_score']:.2f}%")

# Get asset history
history = portfolio.get_asset_history("AAPL", "stock", period="1mo")

# Update asset
portfolio.update_asset(asset_id, quantity=15)

# Remove asset
portfolio.remove_asset(asset_id)
```

### 2. Financial Analysis

```python
from src.financial_analyzer import FinancialAnalyzer

# Initialize analyzer
analyzer = FinancialAnalyzer()

# Analyze a stock
stock_analysis = analyzer.analyze_asset("AAPL", "stock")
print(f"Current Price: ${stock_analysis['price_metrics']['current_price']:,.2f}")
print(f"Volatility: {stock_analysis['price_metrics']['volatility']:.2f}%")
print(f"RSI: {stock_analysis['technical_indicators']['rsi']:.2f}")

# Get market conditions
market = analyzer.get_market_conditions()
print(f"Market Trend: {market['market_trend']}")
print(f"VIX Level: {market['vix_level']:.2f}")
print(f"SPY Performance: {market['spy_performance']:.2f}%")
```

### 3. AI Investment Advisor

```python
from src.ai_insights import AIInvestmentAdvisor

# Initialize AI advisor
advisor = AIInvestmentAdvisor("your_gemini_api_key")

# Get investment advice
portfolio_data = {
    'total_portfolio_value': 100000.0,
    'total_gain_loss': 5000.0,
    'risk_metrics': {
        'volatility': 15.5,
        'diversification_score': 75.0
    },
    'asset_values': [
        {
            'symbol': 'AAPL',
            'current_value': 15000.0,
            'gain_loss': 2000.0
        }
    ]
}

advice = advisor.get_investment_advice(portfolio_data)
print("Portfolio Analysis:", advice['portfolio_analysis']['performance'])
print("Risk Assessment:", advice['portfolio_analysis']['risk_assessment'])
print("Recommendations:", advice['portfolio_analysis']['rebalancing'])

# Get market sentiment analysis
market_data = {
    'market_trend': 'Bullish',
    'volatility': 'Low',
    'spy_performance': 2.5,
    'vix_level': 15.5
}

sentiment = advisor.analyze_market_sentiment(market_data)
print("Market Sentiment:", sentiment['overall_sentiment'])
print("Market Drivers:", sentiment['market_drivers'])
print("Opportunities:", sentiment['opportunities'])

# Get asset recommendations
recommendations = advisor.get_asset_recommendations(
    portfolio_data,
    risk_profile="moderate"
)
print("Recommended Allocation:", recommendations['asset_allocation'])
print("Investment Opportunities:", recommendations['investment_opportunities'])
print("Risk Mitigation:", recommendations['risk_mitigation'])
```

### 4. Finance Chatbot

```python
from src.chatbot import FinanceChatbot

# Initialize chatbot
chatbot = FinanceChatbot("your_gemini_api_key")

# Update context with portfolio and market data
chatbot.update_context('portfolio_data', portfolio_data)
chatbot.update_context('market_data', market_data)

# Stream responses (real-time)
for chunk in chatbot.ask_stream("How is my portfolio performing?"):
    print(chunk, end='', flush=True)  # Print each chunk as it arrives

# Stream portfolio insights
for chunk in chatbot.get_portfolio_insights_stream("What's my risk level?"):
    print(chunk, end='', flush=True)

# Stream market insights
for chunk in chatbot.get_market_insights_stream("How's the market looking?"):
    print(chunk, end='', flush=True)

# Example with async processing
async def process_stream():
    async for chunk in chatbot.ask_stream("What are the top performing assets?"):
        print(chunk, end='', flush=True)
        # Process chunk in real-time
        await process_chunk(chunk)

# Clear chat history
chatbot.clear_history()

# Example of handling streaming response in a UI
def update_ui_with_stream():
    response_area = ""
    for chunk in chatbot.ask_stream("Give me investment advice"):
        response_area += chunk
        # Update UI in real-time
        update_text_area(response_area)
```

### 5. Database Operations

```python
from src.database import Database

# Initialize database
db = Database("data/portfolio.db")

# Add asset
asset_data = {
    'id': 'AAPL_123',
    'symbol': 'AAPL',
    'name': 'Apple Inc.',
    'type': 'stock',
    'quantity': 10,
    'purchase_price': 150.0,
    'purchase_date': '2024-01-01',
    'sector': 'Technology'
}
db.add_asset(asset_data)

# Get all assets
assets = db.get_all_assets()

# Update asset
asset_data['quantity'] = 15
db.update_asset('AAPL_123', asset_data)

# Remove asset
db.remove_asset('AAPL_123')
```

### 6. Technical Analysis

```python
from src.utils import calculate_technical_indicators

# Calculate technical indicators for a price series
indicators = calculate_technical_indicators(price_data)
print(f"RSI: {indicators['rsi']:.2f}")
print(f"SMA 20: {indicators['sma_20']:.2f}")
print(f"SMA 50: {indicators['sma_50']:.2f}")
print(f"MACD: {indicators['macd']:.2f}")
print(f"MACD Signal: {indicators['macd_signal']:.2f}")
```

## Testing

Run all tests:

```bash
python -m pytest tests/ -v
```

Run tests with coverage:

```bash
python -m pytest tests/ -v --cov=src
```

## Project Structure

```
portfolio-management/
├── src/
│   ├── __init__.py
│   ├── portfolio_manager.py   # Core portfolio management
│   ├── financial_analyzer.py  # Financial analysis
│   ├── ai_insights.py        # AI investment advisor
│   ├── chatbot.py           # Finance chatbot
│   ├── database.py          # Data persistence
│   └── utils.py             # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_portfolio_manager.py
│   ├── test_financial_analyzer.py
│   ├── test_ai_insights.py
│   └── test_chatbot.py
├── data/
│   └── portfolio.db         # SQLite database
├── requirements.txt
└── README.md
```

## Error Handling

The library includes comprehensive error handling:

- Invalid API responses
- Database errors
- Network issues
- Invalid input validation
- AI service failures

Each component provides default/fallback behavior when errors occur.

## Best Practices

1. Always initialize components with proper configuration
2. Handle API keys securely using environment variables
3. Regularly backup the database
4. Monitor API rate limits
5. Test in development before production use
6. Handle errors appropriately in your application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
