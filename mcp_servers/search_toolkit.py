import logging
import aiohttp
from typing import Dict, List, Any
import json
import asyncio
from bs4 import BeautifulSoup
import urllib.parse

logger = logging.getLogger(__name__)

class SearchToolkit:
    """Toolkit for performing web searches."""
    
    def __init__(self):
        """Initialize the search toolkit."""
        self.session = None
        
    async def search_google(self, query: str, limit: int = 10) -> List[Dict[str, str]]:
        """Perform a Google search.
        
        Args:
            query: The search query
            limit: The maximum number of results to return
            
        Returns:
            The search results
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Encode the query for URL
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}&num={limit}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            async with self.session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Search request failed with status {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                search_results = []
                for result in soup.select('div.g'):
                    try:
                        title_elem = result.select_one('h3')
                        link_elem = result.select_one('a')
                        snippet_elem = result.select_one('div.VwiC3b')
                        
                        if title_elem and link_elem:
                            title = title_elem.get_text()
                            url = link_elem['href']
                            snippet = snippet_elem.get_text() if snippet_elem else "No snippet available"
                            
                            # Only add if it's a valid URL
                            if url.startswith('http'):
                                search_results.append({
                                    "title": title,
                                    "url": url,
                                    "snippet": snippet
                                })
                                
                                if len(search_results) >= limit:
                                    break
                    except Exception as e:
                        logger.warning(f"Error parsing search result: {str(e)}")
                        continue
                
                return search_results
                    
        except Exception as e:
            logger.error(f"Error performing search: {str(e)}", exc_info=True)
            return []
            
    async def close(self):
        """Close the session."""
        if self.session:
            await self.session.close()
            self.session = None 