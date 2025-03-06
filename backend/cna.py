# Import the NewsCrawler class from the crawl_functions module
from crawl_functions import NewsCrawler

CATEGORY_COUNT = 99  # The total number of news categories to extract; 99 means "ALL categories"
NEWS_PER_CATEGORY = 5  # The number of news articles to extract from each category

# Function to crawl news from CNA (Central News Agency)
def crawl_cna(target=""):
    # Initialize the NewsCrawler with the base URL of the CNA news website
    crawler = NewsCrawler("https://www.cna.com.tw/list/aall.aspx")
    
    # Fetch the homepage and extract available categories or articles
    crawler.fetch_home_page(target)
    
    # Crawl news articles from the specified number of categories and limit the number of articles per category
    crawler.crawl_news_under_cats(
        cat_count=CATEGORY_COUNT,  # Number of categories to crawl
        news_count=NEWS_PER_CATEGORY  # Number of articles to fetch per category
    )
    
    # Save the crawled results to a file or database
    crawler.save_result()