import feedparser
from typing import List, Dict
from camel.types import Tool
from camel.toolkits.base_toolkit import BaseToolkit

class NewsToolkit(BaseToolkit):
    def __init__(self):
        self.name = "NewsToolkit"

    def get_tools(self) -> List[Tool]:
        return [Tool(name="get_news", func=self.get_news, description="Fetch latest news from Google News RSS")]

    def get_news(self, query: str) -> List[Dict[str, str]]:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        results = []

        for entry in feed.entries[:5]:
            results.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            })

        return results 