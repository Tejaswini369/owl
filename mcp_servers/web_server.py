import asyncio
import json
import logging
import os
import sys
import base64
import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random
from search_toolkit import SearchToolkit
from browser_toolkit import BrowserToolkit

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebServer:
    """Server for web operations."""
    
    def __init__(self):
        """Initialize the web server."""
        self.search_toolkit = SearchToolkit()
        self.browser_toolkit = BrowserToolkit()
        
    async def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search the web.
        
        Args:
            query: The search query
            limit: The maximum number of results to return
            
        Returns:
            The search results
        """
        try:
            results = await self.search_toolkit.search_google(query, limit)
            return {
                "status": "success",
                "results": results
            }
        except Exception as e:
            logger.error(f"Error searching: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def extract(self, url: str) -> Dict[str, Any]:
        """Extract content from a URL.
        
        Args:
            url: The URL to extract content from
            
        Returns:
            The extracted content
        """
        try:
            content = await self.browser_toolkit.browser_extract_text(url)
            
            # Encode content as base64 to avoid JSON serialization issues
            encoded_content = base64.b64encode(content.encode()).decode()
            
            return {
                "status": "success",
                "content": encoded_content
            }
        except Exception as e:
            logger.error(f"Error extracting content: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def summarize(self, content: str, length: Optional[int] = None) -> Dict[str, Any]:
        """Summarize content.
        
        Args:
            content: The content to summarize
            length: The desired length of the summary
            
        Returns:
            The summary
        """
        try:
            # Decode content if it's base64 encoded
            if content.startswith("data:text/plain;base64,"):
                content = base64.b64decode(content.split(",")[1]).decode()
            
            summary = await self.browser_toolkit.browser_summarize(content, length)
            
            return {
                "status": "success",
                "summary": summary
            }
        except Exception as e:
            logger.error(f"Error summarizing content: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def fetch_news(self, query: str, sources: Optional[List[str]] = None, limit: int = 10) -> Dict[str, Any]:
        """Fetch news articles.
        
        Args:
            query: The search query
            sources: The news sources to search
            limit: The maximum number of results to return
            
        Returns:
            The news articles
        """
        try:
            # For now, return mock news articles
            # In a real implementation, this would use a news API
            articles = []
            
            # Use the search toolkit to find relevant content
            search_results = await self.search_toolkit.search_google(query, limit)
            
            for i, result in enumerate(search_results):
                # Try to extract content from the URL
                try:
                    content = await self.browser_toolkit.browser_extract_text(result["url"])
                except:
                    content = result["snippet"]
                
                # Create a mock article
                article = {
                    "title": result["title"],
                    "url": result["url"],
                    "source": result.get("source", "Unknown Source"),
                    "date": datetime.now().isoformat(),
                    "content": content
                }
                
                articles.append(article)
            
            return {
                "status": "success",
                "articles": articles,
                "sources_used": sources or ["Google"],
                "total_found": len(articles)
            }
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def filter_news(self, articles: List[Dict[str, Any]], keyword: Optional[str] = None, 
                         start_date: Optional[str] = None, end_date: Optional[str] = None, 
                         limit: Optional[int] = None) -> Dict[str, Any]:
        """Filter news articles.
        
        Args:
            articles: The articles to filter
            keyword: The keyword to filter by
            start_date: The start date to filter by
            end_date: The end date to filter by
            limit: The maximum number of results to return
            
        Returns:
            The filtered articles
        """
        try:
            # Sanitize articles to ensure they can be JSON serialized
            sanitized_articles = []
            for article in articles:
                sanitized_article = {
                    "title": str(article.get("title", "")),
                    "url": str(article.get("url", "")),
                    "source": str(article.get("source", "")),
                    "date": str(article.get("date", "")),
                    "content": str(article.get("content", ""))
                }
                sanitized_articles.append(sanitized_article)
            
            filtered_articles = []
            
            # Apply filters
            for article in sanitized_articles:
                # Keyword filter
                if keyword and keyword.lower() not in article["title"].lower() and keyword.lower() not in article["content"].lower():
                    continue
                
                # Date filter
                if start_date or end_date:
                    try:
                        article_date = datetime.fromisoformat(article["date"].replace("Z", "+00:00"))
                        
                        if start_date:
                            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
                            if article_date < start:
                                continue
                        
                        if end_date:
                            end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                            if article_date > end:
                                continue
                    except:
                        # If date parsing fails, skip date filtering
                        pass
                
                filtered_articles.append(article)
            
            # Apply limit
            if limit:
                filtered_articles = filtered_articles[:limit]
            
            return {
                "status": "success",
                "articles": filtered_articles,
                "total_filtered": len(filtered_articles)
            }
        except Exception as e:
            logger.error(f"Error filtering news: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def close(self):
        """Close the server."""
        await self.search_toolkit.close()
        await self.browser_toolkit.close()

async def main():
    """Main function to run the web server."""
    # Get the port from command line arguments or use default
    port = 9002
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid port: {sys.argv[1]}")
            return
            
    # Create and start the web server
    server = WebServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main()) 