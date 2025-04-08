import asyncio
import logging
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from urllib.parse import quote, urlparse
import feedparser
from datetime import datetime, timedelta
from tools.common.base_client import BaseClient

class NewsClient(BaseClient):
    """Client for fetching and processing news articles using OWL's search capabilities."""
    
    def __init__(self):
        """Initialize the news client."""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.search_toolkit = None
        self.browser_toolkit = None
    
    async def initialize(self) -> None:
        """Initialize the news client with required toolkits."""
        await super().initialize()
        self.search_toolkit = self.owl.get_toolkit("SearchToolkit")
        self.browser_toolkit = self.owl.get_toolkit("BrowserToolkit")
    
    async def cleanup(self) -> None:
        """Clean up the client session."""
        if self.session:
            self.session.close()
    
    async def fetch_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch content from a URL.
        
        Args:
            url: The URL to fetch
            
        Returns:
            Dict containing the fetched content and metadata
        """
        self.logger.debug(f"Fetching URL: {url}")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Extract text content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get text content
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up text (remove extra whitespace)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                'url': url,
                'content': text,
                'status': 'success',
                'content_type': response.headers.get('content-type', 'text/html'),
                'status_code': response.status_code
            }
        except Exception as e:
            return self._handle_error(e, f"Error fetching URL {url}")
    
    async def search_web(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search the web for information.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            Dict containing search results and metadata
        """
        self.logger.debug(f"Searching web for: {query}")
        try:
            # For now, we'll use a simple Google search URL
            search_url = f"https://www.google.com/search?q={quote(query)}"
            response = await self.fetch_url(search_url)
            
            if response['status'] == 'success':
                # Extract search results (this is a simplified version)
                soup = BeautifulSoup(response['content'], 'html.parser')
                results = []
                
                # Find search result elements (this is a simplified approach)
                for result in soup.select('div.g')[:limit]:
                    title_elem = result.select_one('h3')
                    link_elem = result.select_one('a')
                    snippet_elem = result.select_one('div.VwiC3b')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text()
                        link = link_elem.get('href')
                        snippet = snippet_elem.get_text() if snippet_elem else ""
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
                
                return {
                    'query': query,
                    'results': results,
                    'total_results': len(results),
                    'status': 'success'
                }
            else:
                return {
                    'query': query,
                    'results': [],
                    'total_results': 0,
                    'status': 'error',
                    'error': response.get('error', 'Unknown error')
                }
        except Exception as e:
            return self._handle_error(e, "Error searching web")
    
    async def extract_content(self, url: str) -> Dict[str, Any]:
        """
        Extract content from a URL.
        
        Args:
            url: The URL to extract content from
            
        Returns:
            Dict containing the extracted content and metadata
        """
        self.logger.debug(f"Extracting content from: {url}")
        response = await self.fetch_url(url)
        
        if response['status'] == 'success':
            return {
                'url': url,
                'content': response['content'],
                'status': 'success'
            }
        else:
            return {
                'url': url,
                'content': None,
                'status': 'error',
                'error': response.get('error', 'Unknown error')
            }
    
    async def summarize_page(self, url: str) -> Dict[str, Any]:
        """
        Summarize content from a URL.
        
        Args:
            url: The URL to summarize
            
        Returns:
            Dict containing the summary and metadata
        """
        self.logger.debug(f"Summarizing page: {url}")
        response = await self.fetch_url(url)
        
        if response['status'] == 'success':
            # For now, just return the first 500 characters as a summary
            content = response['content']
            summary = content[:500] + "..." if len(content) > 500 else content
            
            return {
                'url': url,
                'summary': summary,
                'status': 'success'
            }
        else:
            return {
                'url': url,
                'summary': None,
                'status': 'error',
                'error': response.get('error', 'Unknown error')
            }
    
    async def discover_topics(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Discover relevant news topics based on user query using OWL's search capabilities.
        
        Args:
            query: User's search query
            limit: Maximum number of topics to return
            
        Returns:
            Dictionary containing discovered topics and their metadata
        """
        try:
            # Use OWL's search to find relevant topics
            search_results = await self.search_toolkit.search_web(
                query=f"latest news topics related to {query}",
                num_results=limit
            )
            
            # Extract and analyze topics from search results
            topics = []
            for result in search_results.get('results', []):
                # Extract topic from title and snippet
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                
                # Use OWL to analyze and extract key topics
                analysis = await self.owl.analyze_text(
                    text=f"{title}\n{snippet}",
                    task="extract_key_topics"
                )
                
                if analysis and 'topics' in analysis:
                    topics.extend(analysis['topics'])
            
            # Remove duplicates and limit results
            unique_topics = list(set(topics))[:limit]
            
            return {
                'topics': unique_topics,
                'query': query,
                'total_found': len(unique_topics)
            }
            
        except Exception as e:
            self.logger.error(f"Error discovering topics: {str(e)}")
            return {
                'topics': [],
                'query': query,
                'error': str(e)
            }
    
    async def fetch_news(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """
        Fetch news articles based on user query.
        
        Args:
            query: User's search query
            limit: Maximum number of articles to return
            
        Returns:
            Dictionary containing articles and metadata
        """
        try:
            # First discover relevant topics
            topics = await self.discover_topics(query, limit=3)
            
            # Use discovered topics to fetch news
            articles = []
            for topic in topics.get('topics', []):
                # Construct Google News RSS URL
                encoded_topic = quote(topic)
                url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
                
                # Fetch and parse RSS feed
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:limit//len(topics.get('topics', [topic]))]:
                    article = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.get('published', ''),
                        'source': entry.get('source', {}).get('title', ''),
                        'summary': entry.get('summary', ''),
                        'topic': topic
                    }
                    articles.append(article)
            
            return {
                'articles': articles[:limit],
                'total_found': len(articles),
                'topics': topics.get('topics', []),
                'query': query
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching news: {str(e)}")
            return {
                'articles': [],
                'error': str(e),
                'query': query
            }
    
    async def filter_news(self, articles: List[Dict], keyword: Optional[str] = None,
                         source: Optional[str] = None, date_from: Optional[str] = None,
                         date_to: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        Filter news articles based on various criteria.
        
        Args:
            articles: List of articles to filter
            keyword: Keyword to filter by
            source: Source to filter by
            date_from: Start date for filtering
            date_to: End date for filtering
            limit: Maximum number of results to return
            
        Returns:
            Dictionary containing filtered articles and metadata
        """
        try:
            filtered = articles.copy()
            
            if keyword:
                filtered = [a for a in filtered if keyword.lower() in a['title'].lower() or 
                          keyword.lower() in a['summary'].lower()]
            
            if source:
                filtered = [a for a in filtered if source.lower() in a['source'].lower()]
            
            if date_from:
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                filtered = [a for a in filtered if datetime.strptime(a['published'], '%a, %d %b %Y %H:%M:%S %z') >= date_from]
            
            if date_to:
                date_to = datetime.strptime(date_to, '%Y-%m-%d')
                filtered = [a for a in filtered if datetime.strptime(a['published'], '%a, %d %b %Y %H:%M:%S %z') <= date_to]
            
            return {
                'articles': filtered[:limit],
                'total_found': len(filtered),
                'original_count': len(articles),
                'filters_applied': {
                    'keyword': keyword,
                    'source': source,
                    'date_from': date_from,
                    'date_to': date_to
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error filtering news: {str(e)}")
            return {
                'articles': [],
                'error': str(e),
                'original_count': len(articles)
            }
    
    async def get_news_sources(self) -> Dict[str, Any]:
        """
        Get list of available news sources from fetched articles.
        
        Returns:
            Dictionary containing list of sources and metadata
        """
        try:
            # Use OWL's search to find popular news sources
            search_results = await self.search_toolkit.search_web(
                query="top news websites and sources",
                num_results=20
            )
            
            sources = set()
            for result in search_results.get('results', []):
                # Extract domain from URL
                url = result.get('link', '')
                domain = re.search(r'https?://(?:www\.)?([^/]+)', url)
                if domain:
                    sources.add(domain.group(1))
            
            return {
                'sources': list(sources),
                'total_found': len(sources)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting news sources: {str(e)}")
            return {
                'sources': [],
                'error': str(e)
            } 