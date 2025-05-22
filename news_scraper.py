import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

class NvidiaNewsScraper:
    def __init__(self):
        # Initialize NewsAPI client
        load_dotenv()
        self.newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))
        
    def get_newsapi_articles(self, days_back=7):
        """Get NVIDIA news from NewsAPI"""
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        articles = self.newsapi.get_everything(
            q='NVIDIA OR "NVIDIA Corporation"',
            from_param=from_date,
            language='en',
            sort_by='relevancy'
        )
        
        return articles['articles']

    def get_reuters_articles(self):
        """Scrape NVIDIA news from Reuters"""
        url = "https://www.reuters.com/search/news?blob=NVIDIA"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = []
            
            # Note: You'll need to adjust these selectors based on Reuters' actual HTML structure
            for article in soup.find_all('div', class_='search-result-content'):
                title = article.find('h3').text.strip()
                date = article.find('time').text.strip()
                articles.append({
                    'title': title,
                    'date': date,
                    'source': 'Reuters'
                })
                
            return articles
        except Exception as e:
            print(f"Error scraping Reuters: {e}")
            return []

    def process_articles(self, articles):
        """Process articles into a DataFrame with sentiment analysis"""
        processed_articles = []
        
        for article in articles:
            processed_articles.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'published_at': article.get('publishedAt', ''),
                'source': article.get('source', {}).get('name', ''),
                'url': article.get('url', '')
            })
            
        df = pd.DataFrame(processed_articles)
        df['published_at'] = pd.to_datetime(df['published_at'])
        return df

    def get_all_news(self):
        """Combine news from all sources"""
        newsapi_articles = self.get_newsapi_articles()
        reuters_articles = self.get_reuters_articles()
        
        all_articles = newsapi_articles + reuters_articles
        df = self.process_articles(all_articles)
        
        # Save to CSV
        df.to_csv('nvidia_news.csv', index=False)
        return df

if __name__ == "__main__":
    scraper = NvidiaNewsScraper()
    news_df = scraper.get_all_news()
    print(f"Scraped {len(news_df)} articles")
