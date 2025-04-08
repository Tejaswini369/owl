"""
News Toolkit for OWL.
This toolkit provides tools for fetching and processing news articles.
"""

import feedparser
import urllib.parse
from typing import Optional, Any
from owl.types import Tool

class NewsToolkit:
    """A toolkit for fetching and processing news articles."""
    
    def __init__(self, llm_client=None):
        """
        Initialize the NewsToolkit.
        
        Args:
            llm_client: Optional LLM client for generating responses (Anthropic, OpenAI, etc.)
        """
        self.llm_client = llm_client
        
    def _get_llm_response(self, messages: list[dict]) -> str:
        """
        Get response from LLM client, handling different client types.
        
        Args:
            messages: List of message dictionaries with role and content
            
        Returns:
            The LLM's response text
        """
        if isinstance(self.llm_client, type(None)):
            raise ValueError("LLM client is required")
            
        # Handle Anthropic client
        if self.llm_client.__class__.__name__ == "Anthropic":
            # Convert messages to Anthropic format
            system_message = next((m["content"] for m in messages if m["role"] == "system"), "")
            user_message = next((m["content"] for m in messages if m["role"] == "user"), "")
            
            response = self.llm_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                system=system_message,
                messages=[{"role": "user", "content": user_message}]
            )
            return response.content[0].text
            
        # Handle OpenAI client
        elif self.llm_client.__class__.__name__ == "OpenAI":
            response = self.llm_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                max_tokens=1024,
                messages=messages
            )
            return response.choices[0].message.content
            
        else:
            raise ValueError(f"Unsupported LLM client type: {type(self.llm_client)}")
        
    def get_tools(self) -> list[Tool]:
        """
        Get the list of tools provided by this toolkit.
        
        Returns:
            A list of Tool objects.
        """
        return [
            Tool(
                name="get_news",
                description="Fetch news articles based on a query",
                func=self.get_news,
                parameters={
                    "query": {
                        "type": "string",
                        "description": "The search query for news articles"
                    }
                }
            ),
            Tool(
                name="process_news_query",
                description="Process a user's news query and generate a response",
                func=self.process_news_query,
                parameters={
                    "user_query": {
                        "type": "string",
                        "description": "The user's news-related question"
                    }
                }
            )
        ]
        
    def get_news(self, query: str) -> list[dict]:
        """
        Fetch news articles based on a query.
        
        Args:
            query: The search query for news articles
            
        Returns:
            A list of dictionaries containing news article information
        """
        # URL encode the query
        encoded_query = urllib.parse.quote(query)
        
        # Use Google News RSS feed
        url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        
        articles = []
        for entry in feed.entries:
            article = {
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "Unknown date"),
                "summary": entry.get("summary", "No summary available")
            }
            articles.append(article)
            
        return articles
        
    def process_news_query(self, user_query: str) -> dict:
        """
        Process a user's news query and generate a response.
        
        Args:
            user_query: The user's news-related question
            
        Returns:
            A dictionary containing the response and relevant articles
        """
        if not self.llm_client:
            raise ValueError("LLM client is required for processing news queries. Please initialize NewsToolkit with an LLM client.")
            
        # Extract key terms from the user query using the LLM
        system_prompt = """
        You are a helpful AI assistant that extracts relevant search terms from user queries about news.
        Extract only the most important keywords that would be useful for searching news articles.
        Return only the keywords, nothing else.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Extract search terms from: {user_query}"}
        ]
        
        search_terms = self._get_llm_response(messages).strip()
        
        # Fetch news articles using the extracted terms
        articles = self.get_news(search_terms)
        
        if not articles:
            return {
                "response": "I couldn't find any relevant news articles for your query.",
                "articles": []
            }
            
        # Generate a response using the LLM based on the articles
        article_summaries = "\n\n".join([
            f"Title: {article['title']}\nSummary: {article['summary']}\nPublished: {article['published']}"
            for article in articles[:5]  # Use top 5 articles for context
        ])
        
        system_prompt = """
        You are a helpful AI assistant that provides news updates. Based on the provided news articles,
        generate a concise and informative response to the user's query. Include relevant information
        from the articles and cite your sources.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User Query: {user_query}\n\nAvailable Articles:\n{article_summaries}"}
        ]
        
        response = self._get_llm_response(messages)
        
        return {
            "response": response,
            "articles": articles[:5]  # Return top 5 articles for reference
        } 