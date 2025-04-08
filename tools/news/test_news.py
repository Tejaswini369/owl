import logging
from owl.toolkits.news_toolkit import NewsToolkit

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_input() -> dict:
    """Get search parameters from user input."""
    print("\n=== News Search Interface ===")
    query = input("\nEnter your search query").strip()
    
    # Get optional filters
    print("\nOptional filters (press Enter to skip):")
    filter_keyword = input("Enter specific keyword to filter results: ").strip()
    
    try:
        limit = int(input("Enter number of articles to display (default is 5): ").strip() or "5")
    except ValueError:
        limit = 5
        print("Invalid number, using default value of 5")
    
    return {
        'query': query,
        'filter_keyword': filter_keyword if filter_keyword else None,
        'limit': limit
    }

def display_articles(articles, limit=5):
    """Display articles in a formatted way."""
    print(f"\nDisplaying {min(len(articles), limit)} of {len(articles)} articles:\n")
    
    for i, article in enumerate(articles[:limit], 1):
        print(f"\nArticle {i}:")
        print(f"Title: {article.get('title', 'No title')}")
        print(f"Published: {article.get('published', 'No date')}")
        print(f"Link: {article.get('link', 'No link')}")
        print("-" * 80)

def main():
    # Initialize the news toolkit
    news_toolkit = NewsToolkit()
    
    # Get user input
    params = get_user_input()
    
    if not params['query']:
        logger.error("No search query provided")
        return
    
    logger.info(f"\nFetching news for query: {params['query']}...")
    
    # Fetch articles
    articles = news_toolkit.get_news(params['query'])
    
    if not articles:
        logger.error("No articles found")
        return
    
    logger.info(f"Found {len(articles)} articles")
    
    # Display initial results
    display_articles(articles, params['limit'])
    
    # Apply keyword filter if specified
    if params['filter_keyword']:
        filtered_articles = []
        keyword = params['filter_keyword'].lower()
        
        for article in articles:
            title = article.get('title', '').lower()
            summary = article.get('summary', '').lower()
            link = article.get('link', '').lower()
            
            if (keyword in title or 
                keyword in summary or 
                keyword in link):
                filtered_articles.append(article)
        
        logger.info(f"\nFiltering results with keyword '{params['filter_keyword']}'...")
        logger.info(f"Found {len(filtered_articles)} matching articles")
        
        if filtered_articles:
            display_articles(filtered_articles, params['limit'])
        else:
            print(f"\nNo articles found matching the keyword '{params['filter_keyword']}'")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSearch cancelled by user")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        print("\nThank you for using the news search tool!") 