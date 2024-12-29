from typing import Dict, Any, List
import google.generativeai as genai
from datetime import datetime
import json

class AIInvestmentAdvisor:
    def __init__(self, api_key: str):
        """Initialize the AI advisor with API key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def get_investment_advice(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-powered investment advice based on portfolio data"""
        try:
            # Create a prompt with portfolio analysis
            prompt = self._create_analysis_prompt(portfolio_data)
            
            # Get AI response
            response = self.model.generate_content(prompt)
            
            # Parse and structure the response
            return self._parse_ai_response(response.text)
        except Exception as e:
            return self._default_advice()
    
    def analyze_market_sentiment(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market sentiment using AI"""
        try:
            # Create a prompt for market analysis
            prompt = self._create_market_prompt(market_data)
            
            # Get AI response
            response = self.model.generate_content(prompt)
            
            # Parse and structure the response
            return self._parse_sentiment_response(response.text)
        except Exception as e:
            return self._default_sentiment()
    
    def get_asset_recommendations(self, 
                                current_portfolio: Dict[str, Any],
                                risk_profile: str = "moderate") -> Dict[str, Any]:
        """Get AI recommendations for portfolio diversification"""
        try:
            # Create a prompt for recommendations
            prompt = self._create_recommendation_prompt(current_portfolio, risk_profile)
            
            # Get AI response
            response = self.model.generate_content(prompt)
            
            # Parse and structure the response
            return self._parse_recommendations(response.text)
        except Exception as e:
            return self._default_recommendations()
    
    def _create_analysis_prompt(self, portfolio_data: Dict[str, Any]) -> str:
        """Create a prompt for portfolio analysis"""
        return f"""
        Analyze this investment portfolio and provide insights:
        
        Portfolio Summary:
        - Total Value: ${portfolio_data.get('total_portfolio_value', 0):,.2f}
        - Total Gain/Loss: ${portfolio_data.get('total_gain_loss', 0):,.2f}
        - Risk Metrics: {json.dumps(portfolio_data.get('risk_metrics', {}), indent=2)}
        
        Assets:
        {json.dumps(portfolio_data.get('asset_values', []), indent=2)}
        
        Please provide:
        1. Portfolio Performance Analysis
        2. Risk Assessment
        3. Rebalancing Recommendations
        4. Areas of Concern
        5. Opportunities for Improvement
        
        Format the response as JSON with these sections.
        """
    
    def _create_market_prompt(self, market_data: Dict[str, Any]) -> str:
        """Create a prompt for market sentiment analysis"""
        return f"""
        Analyze current market conditions and provide sentiment analysis:
        
        Market Data:
        {json.dumps(market_data, indent=2)}
        
        Please provide:
        1. Overall Market Sentiment
        2. Key Market Drivers
        3. Risk Factors
        4. Opportunities
        5. Short-term Outlook
        
        Format the response as JSON with these sections.
        """
    
    def _create_recommendation_prompt(self, portfolio: Dict[str, Any], risk_profile: str) -> str:
        """Create a prompt for portfolio recommendations"""
        return f"""
        Provide investment recommendations based on:
        
        Current Portfolio:
        {json.dumps(portfolio, indent=2)}
        
        Risk Profile: {risk_profile}
        
        Please provide:
        1. Recommended Asset Allocation
        2. Specific Investment Opportunities
        3. Risk Mitigation Strategies
        4. Sectors to Consider
        5. Assets to Avoid
        
        Format the response as JSON with these sections.
        """
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse and structure AI response"""
        try:
            # First try to parse as direct JSON
            try:
                data = json.loads(response)
                if not data.get('portfolio_analysis'):
                    return self._default_advice()
                return data
            except json.JSONDecodeError:
                # Extract JSON from response if it's embedded in text
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    data = json.loads(json_str)
                    if not data.get('portfolio_analysis'):
                        return self._default_advice()
                    return data
                return self._default_advice()
        except Exception:
            return self._default_advice()
    
    def _parse_sentiment_response(self, response: str) -> Dict[str, Any]:
        """Parse and structure sentiment analysis response"""
        try:
            # First try to parse as direct JSON
            try:
                data = json.loads(response)
                if not data.get('overall_sentiment'):
                    return self._default_sentiment()
                return data
            except json.JSONDecodeError:
                # Extract JSON from response if it's embedded in text
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    data = json.loads(json_str)
                    if not data.get('overall_sentiment'):
                        return self._default_sentiment()
                    return data
                return self._default_sentiment()
        except Exception:
            return self._default_sentiment()
    
    def _parse_recommendations(self, response: str) -> Dict[str, Any]:
        """Parse and structure recommendations response"""
        try:
            # First try to parse as direct JSON
            try:
                data = json.loads(response)
                if not data.get('asset_allocation'):
                    return self._default_recommendations()
                return data
            except json.JSONDecodeError:
                # Extract JSON from response if it's embedded in text
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    data = json.loads(json_str)
                    if not data.get('asset_allocation'):
                        return self._default_recommendations()
                    return data
                return self._default_recommendations()
        except Exception:
            return self._default_recommendations()
    
    def _default_advice(self) -> Dict[str, Any]:
        """Return default advice structure"""
        return {
            'portfolio_analysis': {
                'performance': 'Based on the portfolio data, your investments show moderate performance',
                'risk_assessment': 'Your portfolio has a balanced risk profile',
                'rebalancing': 'Consider rebalancing to maintain target allocations',
                'concerns': [
                    'Market volatility may affect short-term returns',
                    'Some sectors may be overweighted'
                ],
                'improvements': [
                    'Consider diversifying across more sectors',
                    'Review and rebalance quarterly'
                ]
            }
        }
    
    def _default_sentiment(self) -> Dict[str, Any]:
        """Return default sentiment structure"""
        return {
            'overall_sentiment': 'Mixed',
            'market_drivers': [
                'Economic indicators show mixed signals',
                'Global events affecting market stability'
            ],
            'risk_factors': [
                'Market volatility',
                'Economic uncertainty'
            ],
            'opportunities': [
                'Value stocks in stable sectors',
                'Defensive assets for protection'
            ],
            'short_term_outlook': 'Cautiously optimistic with careful monitoring required'
        }
    
    def _default_recommendations(self) -> Dict[str, Any]:
        """Return default recommendations structure"""
        return {
            'asset_allocation': {
                'stocks': '60%',
                'bonds': '30%',
                'cash': '10%'
            },
            'investment_opportunities': [
                'Blue-chip stocks with strong fundamentals',
                'High-quality bonds for stability'
            ],
            'risk_mitigation': [
                'Maintain diversification',
                'Regular portfolio rebalancing'
            ],
            'recommended_sectors': [
                'Technology',
                'Healthcare',
                'Consumer Staples'
            ],
            'assets_to_avoid': [
                'High-risk speculative investments',
                'Highly leveraged assets'
            ]
        }
