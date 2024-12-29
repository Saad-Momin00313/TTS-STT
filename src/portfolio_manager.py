from typing import Dict, Any, List, Optional
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from src.database import Database
from src.utils import calculate_technical_indicators, get_asset_info, calculate_correlation

class PortfolioManager:
    def __init__(self, db_path: str = "data/portfolio.db"):
        """Initialize the portfolio manager with database connection"""
        self.db = Database(db_path)
    
    def add_asset(self, symbol: str, asset_type: str, quantity: float, purchase_price: float) -> str:
        """Add a new asset to the portfolio"""
        asset_info = get_asset_info(symbol, asset_type)
        asset_id = f"{symbol}_{datetime.now().timestamp()}"
        
        asset_data = {
            'id': asset_id,
            'symbol': symbol,
            'name': asset_info.get('name', symbol),
            'type': asset_type,
            'quantity': quantity,
            'purchase_price': purchase_price,
            'purchase_date': datetime.now().isoformat(),
            'sector': asset_info.get('sector', 'Other'),
            'metadata': asset_info.get('metadata', {})
        }
        
        if self.db.add_asset(asset_data):
            return asset_id
        return None
    
    def remove_asset(self, asset_id: str) -> bool:
        """Remove an asset from the portfolio"""
        return self.db.remove_asset(asset_id)
    
    def update_asset(self, asset_id: str, quantity: Optional[float] = None, 
                    purchase_price: Optional[float] = None) -> bool:
        """Update asset details"""
        assets = self.db.get_all_assets()
        if asset_id not in assets:
            return False
        
        asset_data = assets[asset_id]
        if quantity is not None:
            asset_data['quantity'] = quantity
        if purchase_price is not None:
            asset_data['purchase_price'] = purchase_price
        
        return self.db.update_asset(asset_id, asset_data)
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get complete portfolio summary with current values and metrics"""
        assets = self.db.get_all_assets()
        if not assets:
            return self._empty_portfolio_summary()
        
        total_value = 0
        total_cost = 0
        asset_values = []
        
        for asset in assets.values():
            current_price = self._get_current_price(asset['symbol'], asset['type'])
            if current_price:
                asset_value = current_price * asset['quantity']
                total_value += asset_value
                total_cost += asset['purchase_price'] * asset['quantity']
                asset_values.append({
                    'id': asset['id'],
                    'symbol': asset['symbol'],
                    'current_value': asset_value,
                    'current_price': current_price,
                    'quantity': asset['quantity'],
                    'purchase_price': asset['purchase_price'],
                    'gain_loss': asset_value - (asset['purchase_price'] * asset['quantity']),
                    'gain_loss_percentage': ((current_price / asset['purchase_price']) - 1) * 100
                })
        
        return {
            'total_portfolio_value': total_value,
            'total_cost_basis': total_cost,
            'total_gain_loss': total_value - total_cost,
            'total_gain_loss_percentage': ((total_value / total_cost) - 1) * 100 if total_cost > 0 else 0,
            'asset_values': asset_values,
            'risk_metrics': self._calculate_risk_metrics(assets),
            'performance_metrics': self._calculate_performance_metrics(assets)
        }
    
    def get_asset_history(self, symbol: str, asset_type: str, period: str = "1mo") -> pd.DataFrame:
        """Get historical data for an asset"""
        if asset_type.lower() == 'stock':
            ticker = yf.Ticker(symbol)
            return ticker.history(period=period)
        return pd.DataFrame()  # Implement crypto history if needed
    
    def _get_current_price(self, symbol: str, asset_type: str) -> float:
        """Get current price for an asset"""
        try:
            if asset_type.lower() == 'stock':
                ticker = yf.Ticker(symbol)
                return ticker.info.get('regularMarketPrice', 0)
            # Implement crypto price fetching if needed
            return 0
        except Exception:
            return 0
    
    def _calculate_risk_metrics(self, assets: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """Calculate portfolio risk metrics"""
        if not assets:
            return {'volatility': 0, 'diversification_score': 0}
        
        # Calculate portfolio volatility
        returns = []
        for asset in assets.values():
            history = self.get_asset_history(asset['symbol'], asset['type'])
            if not history.empty:
                asset_returns = history['Close'].pct_change().dropna()
                returns.append(asset_returns)
        
        if returns:
            portfolio_returns = pd.concat(returns, axis=1)
            volatility = portfolio_returns.std().mean() * 100
        else:
            volatility = 0
        
        # Calculate diversification score
        correlation = calculate_correlation(assets)
        diversification_score = (1 - abs(correlation)) * 100
        
        return {
            'volatility': volatility,
            'diversification_score': diversification_score
        }
    
    def _calculate_performance_metrics(self, assets: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
        """Calculate portfolio performance metrics"""
        if not assets:
            return {'sharpe_ratio': 0, 'beta': 0}
        
        # Calculate portfolio returns
        portfolio_returns = []
        for asset in assets.values():
            history = self.get_asset_history(asset['symbol'], asset['type'])
            if not history.empty:
                returns = history['Close'].pct_change().dropna()
                portfolio_returns.append(returns)
        
        if not portfolio_returns:
            return {'sharpe_ratio': 0, 'beta': 0}
        
        portfolio_returns = pd.concat(portfolio_returns, axis=1).mean(axis=1)
        
        # Calculate Sharpe ratio (assuming risk-free rate of 2%)
        risk_free_rate = 0.02
        excess_returns = portfolio_returns - risk_free_rate/252
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / portfolio_returns.std()
        
        # Calculate portfolio beta
        market = yf.Ticker("SPY").history(period="1y")['Close'].pct_change().dropna()
        if len(market) == len(portfolio_returns):
            covariance = portfolio_returns.cov(market)
            market_variance = market.var()
            beta = covariance / market_variance if market_variance != 0 else 0
        else:
            beta = 0
        
        return {
            'sharpe_ratio': sharpe_ratio,
            'beta': beta
        }
    
    def _empty_portfolio_summary(self) -> Dict[str, Any]:
        """Return empty portfolio summary structure"""
        return {
            'total_portfolio_value': 0,
            'total_cost_basis': 0,
            'total_gain_loss': 0,
            'total_gain_loss_percentage': 0,
            'asset_values': [],
            'risk_metrics': {'volatility': 0, 'diversification_score': 0},
            'performance_metrics': {'sharpe_ratio': 0, 'beta': 0}
        }
