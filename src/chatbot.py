from typing import Dict, Any, List, Optional, Generator, Iterator
import google.generativeai as genai
import json
import time

class FinanceChatbot:
    def __init__(self, api_key: str):
        """Initialize the finance chatbot"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.context = {
            'portfolio_data': None,
            'market_data': None,
            'chat_history': []
        }
    
    def ask_stream(self, question: str) -> Iterator[str]:
        """Process a user question and stream the response"""
        try:
            # Create a prompt with context and question
            prompt = self._create_chat_prompt(question)
            
            # Get streaming response from AI
            response = self.model.generate_content(
                prompt,
                stream=True  # Enable streaming
            )
            
            # Initialize the complete response for history
            complete_response = ""
            
            # Stream the response chunks
            for chunk in response:
                if chunk.text:
                    complete_response += chunk.text
                    yield chunk.text
            
            # Parse the complete response and update history
            try:
                parsed_response = self._parse_response(complete_response)
                self.context['chat_history'].append({
                    'question': question,
                    'response': parsed_response
                })
            except Exception:
                # If parsing fails, create a default response for history
                default_response = self._default_response("Response parsing failed")
                self.context['chat_history'].append({
                    'question': question,
                    'response': default_response
                })
                
        except Exception as e:
            # Yield error message in case of failure
            error_msg = f"I apologize, but I'm having trouble processing your request: {str(e)}"
            yield error_msg
            
            # Update history with default response
            default_response = self._default_response(error_msg)
            self.context['chat_history'].append({
                'question': question,
                'response': default_response
            })
    
    def get_portfolio_insights_stream(self, question: str) -> Iterator[str]:
        """Get streaming insights about the portfolio"""
        if not self.context.get('portfolio_data'):
            yield "I don't have any portfolio data to analyze."
            return
        
        try:
            prompt = self._create_portfolio_prompt(question)
            response = self.model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    yield chunk.text
                elif isinstance(chunk, dict) and 'text' in chunk:
                    yield chunk['text']
                elif isinstance(chunk, str):
                    yield chunk
                    
        except Exception as e:
            yield f"I couldn't analyze the portfolio data: {str(e)}"
    
    def get_market_insights_stream(self, question: str) -> Iterator[str]:
        """Get streaming insights about market conditions"""
        if not self.context.get('market_data'):
            yield "I don't have any market data to analyze."
            return
        
        try:
            prompt = self._create_market_prompt(question)
            response = self.model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    yield chunk.text
                elif isinstance(chunk, dict) and 'text' in chunk:
                    yield chunk['text']
                elif isinstance(chunk, str):
                    yield chunk
                    
        except Exception as e:
            yield f"I couldn't analyze the market data: {str(e)}"
    
    def update_context(self, context_type: str, data: Dict[str, Any]) -> None:
        """Update chatbot context with new data"""
        if context_type in self.context:
            self.context[context_type] = data
    
    def clear_history(self) -> None:
        """Clear chat history"""
        self.context['chat_history'] = []
    
    def _create_chat_prompt(self, question: str) -> str:
        """Create a context-aware chat prompt"""
        prompt = "You are a financial advisor chatbot. "
        
        # Add portfolio context if available
        if self.context['portfolio_data']:
            prompt += f"\nPortfolio Context:\n{json.dumps(self.context['portfolio_data'], indent=2)}"
        
        # Add market context if available
        if self.context['market_data']:
            prompt += f"\nMarket Context:\n{json.dumps(self.context['market_data'], indent=2)}"
        
        # Add chat history for context
        if self.context['chat_history']:
            prompt += "\nPrevious Conversation:"
            for entry in self.context['chat_history'][-3:]:  # Last 3 exchanges
                prompt += f"\nQ: {entry['question']}\nA: {json.dumps(entry['response'])}"
        
        prompt += f"\n\nUser Question: {question}\n\nProvide a natural, conversational response that includes relevant data points and insights."
        
        return prompt
    
    def _create_portfolio_prompt(self, question: str) -> str:
        """Create a portfolio-specific prompt"""
        return f"""
        Analyze this portfolio data and answer the question in a natural, conversational way:
        
        Portfolio Data:
        {json.dumps(self.context['portfolio_data'], indent=2)}
        
        Question: {question}
        """
    
    def _create_market_prompt(self, question: str) -> str:
        """Create a market-specific prompt"""
        return f"""
        Analyze this market data and answer the question in a natural, conversational way:
        
        Market Data:
        {json.dumps(self.context['market_data'], indent=2)}
        
        Question: {question}
        """
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse and structure the AI response"""
        try:
            # Try to find and parse JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # If no JSON found, create a structured response
                return {
                    'answer': response.strip(),
                    'confidence': 'Medium',
                    'data_points': [],
                    'suggestions': [],
                    'disclaimer': 'This response was generated in streaming mode.'
                }
        except Exception:
            return self._default_response("Response parsing failed")
    
    def _default_response(self, message: str) -> Dict[str, Any]:
        """Return a default response structure"""
        return {
            'answer': message,
            'confidence': 'Low',
            'data_points': [],
            'suggestions': ['Try rephrasing your question'],
            'disclaimer': 'This is a fallback response due to processing issues.'
        }