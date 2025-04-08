import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import requests
from ..common.base_client import BaseClient

class StocksClient(BaseClient):
    """Client for fetching stock market information."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the stocks client.
        
        Args:
            api_key: Optional API key for stock market service
        """
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://api.example.com/v1"  # Replace with actual API endpoint
        self.session = None
    
    async def initialize(self) -> None:
        """Initialize the client session."""
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
            })
    
    async def cleanup(self) -> None:
        """Clean up the client session."""
        if self.session:
            self.session.close()
    
    async def get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current stock price for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., AAPL, GOOGL)
            
        Returns:
            Dict containing stock price information
        """
        self.logger.debug(f"Getting stock price for: {symbol}")
        
        try:
            response = self.session.get(
                f"{self.base_url}/quote",
                params={'symbol': symbol}
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                'symbol': symbol,
                'price': data['price'],
                'change': data['change'],
                'change_percent': data['change_percent'],
                'volume': data['volume'],
                'last_updated': data['timestamp'],
                'status': 'success'
            }
        except Exception as e:
            return self._handle_error(e, f"Error getting stock price for {symbol}")
    
    async def get_stock_history(self, symbol: str, days: int = 30) -> Dict[str, Any]:
        """
        Get historical stock data for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., AAPL, GOOGL)
            days: Number of days of history to retrieve
            
        Returns:
            Dict containing historical stock data
        """
        self.logger.debug(f"Getting {days} days of history for: {symbol}")
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            response = self.session.get(
                f"{self.base_url}/history",
                params={
                    'symbol': symbol,
                    'from': start_date.strftime('%Y-%m-%d'),
                    'to': end_date.strftime('%Y-%m-%d')
                }
            )
            response.raise_for_status()
            
            data = response.json()
            history = []
            
            for day in data['history']:
                history.append({
                    'date': day['date'],
                    'open': day['open'],
                    'high': day['high'],
                    'low': day['low'],
                    'close': day['close'],
                    'volume': day['volume']
                })
            
            return {
                'symbol': symbol,
                'history': history,
                'status': 'success'
            }
        except Exception as e:
            return self._handle_error(e, f"Error getting history for {symbol}")
    
    async def get_market_summary(self) -> Dict[str, Any]:
        """
        Get summary of market indices.
        
        Returns:
            Dict containing market summary information
        """
        self.logger.debug("Getting market summary")
        
        try:
            response = self.session.get(f"{self.base_url}/market/summary")
            response.raise_for_status()
            
            data = response.json()
            indices = []
            
            for index in data['indices']:
                indices.append({
                    'name': index['name'],
                    'value': index['value'],
                    'change': index['change'],
                    'change_percent': index['change_percent']
                })
            
            return {
                'indices': indices,
                'status': 'success'
            }
        except Exception as e:
            return self._handle_error(e, "Error getting market summary")
    
    async def search_stocks(self, query: str) -> Dict[str, Any]:
        """
        Search for stocks matching a query.
        
        Args:
            query: Search query (company name or symbol)
            
        Returns:
            Dict containing matching stocks
        """
        self.logger.debug(f"Searching stocks for: {query}")
        
        try:
            response = self.session.get(
                f"{self.base_url}/search",
                params={'q': query}
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for stock in data['results']:
                results.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'exchange': stock['exchange'],
                    'type': stock['type']
                })
            
            return {
                'query': query,
                'results': results,
                'status': 'success'
            }
        except Exception as e:
            return self._handle_error(e, f"Error searching stocks for {query}")
    
    async def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get detailed company information.
        
        Args:
            symbol: Stock symbol (e.g., AAPL, GOOGL)
            
        Returns:
            Dict containing company information
        """
        self.logger.debug(f"Getting company info for: {symbol}")
        
        try:
            response = self.session.get(
                f"{self.base_url}/company/{symbol}"
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                'symbol': symbol,
                'name': data['name'],
                'description': data['description'],
                'sector': data['sector'],
                'industry': data['industry'],
                'employees': data['employees'],
                'website': data['website'],
                'status': 'success'
            }
        except Exception as e:
            return self._handle_error(e, f"Error getting company info for {symbol}") 