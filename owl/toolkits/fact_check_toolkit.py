"""
Fact Check Toolkit for OWL.
This toolkit provides tools for verifying facts using search APIs.
"""

import os
import urllib.parse
import requests
from typing import Optional, Dict, Any, List
from owl.types import Tool

class FactCheckToolkit:
    """A toolkit for verifying facts using search APIs."""
    
    def __init__(self, llm_client=None, api_key=None):
        """
        Initialize the FactCheckToolkit.
        
        Args:
            llm_client: Optional LLM client for generating responses
            api_key: Optional API key for search services
        """
        self.llm_client = llm_client
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        
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
                name="search_google",
                description="Search Google for current information on a topic",
                func=self.search_google,
                parameters={
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                }
            ),
            Tool(
                name="verify_fact",
                description="Verify a factual claim using search results",
                func=self.verify_fact,
                parameters={
                    "claim": {
                        "type": "string",
                        "description": "The factual claim to verify"
                    }
                }
            )
        ]
    
    def search_google(self, query: str) -> Dict[str, Any]:
        """
        Search Google for information on a topic.
        
        Args:
            query: The search query
            
        Returns:
            A dictionary containing search results
        """
        if not self.api_key:
            # Fallback to a simple web request if no API key is available
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(url, headers=headers)
            
            # This is a simplified approach - in a real implementation,
            # you would parse the HTML to extract search results
            return {
                "query": query,
                "results": [{"title": "Google Search Results", "link": url}],
                "source": "Google Web Search"
            }
        
        # Use SerpAPI if available
        try:
            import serpapi
            
            search = serpapi.GoogleSearch({
                "q": query,
                "api_key": self.api_key,
                "num": 5  # Limit to top 5 results
            })
            results = search.get_dict()
            
            # Extract organic results
            organic_results = results.get("organic_results", [])
            
            return {
                "query": query,
                "results": [
                    {
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "snippet": result.get("snippet", "")
                    }
                    for result in organic_results
                ],
                "source": "SerpAPI"
            }
        except ImportError:
            # Fallback if serpapi is not installed
            return self.search_google(query)
    
    def verify_fact(self, claim: str) -> Dict[str, Any]:
        """
        Verify a factual claim using search results.
        
        Args:
            claim: The factual claim to verify
            
        Returns:
            A dictionary containing the verification result
        """
        if not self.llm_client:
            raise ValueError("LLM client is required for fact verification")
        
        # Search for information related to the claim
        search_results = self.search_google(claim)
        
        # Format search results for the LLM
        results_text = "\n\n".join([
            f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result.get('snippet', 'No snippet available')}"
            for result in search_results.get("results", [])
        ])
        
        # Prompt the LLM to verify the claim
        system_prompt = """
        You are a fact-checking assistant. Your task is to verify the factual claim provided by the user
        using the search results. Determine if the claim is true, false, or partially true based on
        the most recent and reliable information available.
        
        Provide a clear verdict (TRUE, FALSE, or PARTIALLY TRUE) and explain your reasoning.
        Cite specific sources from the search results to support your conclusion.
        If the information is ambiguous or conflicting, acknowledge this and explain why.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Claim to verify: {claim}\n\nSearch Results:\n{results_text}"}
        ]
        
        verification = self._get_llm_response(messages)
        
        return {
            "claim": claim,
            "verification": verification,
            "sources": search_results.get("results", [])
        } 