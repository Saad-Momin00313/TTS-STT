from typing import Dict, Any, List
import yfinance as yf
import pandas as pd
import numpy as np
from src.utils import calculate_technical_indicators

class FinancialAnalyzer:
    def __init__(self):
        """Initialize the financial analyzer"""
        pass
    
    def analyze_asset(self, symbol: str, asset_type: str) -> Dict[str, Any]:
        """Perform comprehensive analysis of an asset"""
        if asset_type.lower() == 'stock':
            return self._analyze_stock(symbol)
        elif asset_type.lower() == 'crypto':
            return self._analyze_crypto(symbol)
        return self._empty_analysis()
    
    def get_market_conditions(self) -> Dict[str, Any]:
        """Analyze overall market conditions"""
        try:
            spy = yf.Ticker("SPY")
            vix = yf.Ticker("^VIX")
            
            spy_hist = spy.history(period="1mo")
            vix_hist = vix.history(period="1mo")
            
            if spy_hist.empty or vix_hist.empty:
                return self._default_market_conditions()
            
            spy_returns = spy_hist['Close'].pct_change().dropna()
            current_vix = vix_hist['Close'].iloc[-1]
            
            market_trend = "Bullish" if spy_returns.mean() > 0 else "Bearish"
            volatility = "High" if current_vix > 20 else "Low"
            
            return {
                'market_trend': market_trend,
                'volatility': volatility,
                'spy_performance': spy_returns.mean() * 100,
                'vix_level': current_vix,
                'technical_indicators': calculate_technical_indicators(spy_hist['Close'])
            }
        except Exception:
            return self._default_market_conditions()
    
    def _analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """Analyze a stock"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1mo")
            
            if hist.empty:
                return self._empty_analysis()
            
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100
            
            analysis = {
                'price_metrics': {
                    'current_price': hist['Close'].iloc[-1],
                    'price_change': returns.iloc[-1] * 100,
                    'volatility': volatility
                },
                'technical_indicators': calculate_technical_indicators(hist['Close']),
                'volume_analysis': {
                    'average_volume': hist['Volume'].mean(),
                    'volume_trend': "Up" if hist['Volume'].iloc[-1] > hist['Volume'].mean() else "Down"
                }
            }
            
            # Add fundamental data if available
            info = ticker.info
            if info:
                analysis['fundamentals'] = {
                    'market_cap': info.get('marketCap'),
                    'pe_ratio': info.get('trailingPE'),
                    'dividend_yield': info.get('dividendYield'),
                    'beta': info.get('beta')
                }
            
            return analysis
        except Exception:
            return self._empty_analysis()
    
    def _analyze_crypto(self, symbol: str) -> Dict[str, Any]:
        """Analyze a cryptocurrency"""
        # Implement crypto analysis if needed
        return self._empty_analysis()
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure"""
        return {
            'price_metrics': {
                'current_price': 0,
                'price_change': 0,
                'volatility': 0
            },
            'technical_indicators': {
                'rsi': 0,
                'sma_50': 0,
                'sma_20': 0,
                'ema_20': 0,
                'macd': 0,
                'macd_signal': 0
            },
            'volume_analysis': {
                'average_volume': 0,
                'volume_trend': "Unknown"
            },
            'fundamentals': {
                'market_cap': None,
                'pe_ratio': None,
                'dividend_yield': None,
                'beta': None
            }
        }
    
    def _default_market_conditions(self) -> Dict[str, Any]:
        """Return default market conditions"""
        return {
            'market_trend': "Unknown",
            'volatility': "Unknown",
            'spy_performance': 0,
            'vix_level': 0,
            'technical_indicators': {
                'rsi': 0,
                'sma_50': 0,
                'sma_20': 0,
                'ema_20': 0,
                'macd': 0,
                'macd_signal': 0
            }
        }
