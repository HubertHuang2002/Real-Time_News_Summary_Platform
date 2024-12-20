import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import chardet
import json

# Define target categories for news crawling
target_cats = [
    "aipl", "aopl", "acn", "aie",  # Various categories such as politics, opinion, etc.
    "asc", "ait", "ahel", "asoc", "aloc",  # Categories for social and local news
    "acul", "aspt", "amov"  # Categories for culture, sports, and movies
]

# Define the NewsCrawler class for crawling CNA news
class NewsCrawler:
    def __init__(self, base_url):
        # Initialize with base URL and other settings
        self.base_url = base_url
        self.domain = "https://www.cna.com.tw"
        self.ua = UserAgent()  # Create a UserAgent instance for generating random headers
        self.headers = {  # HTTP headers for requests
            "User-Agent": self.ua.chrome,  # Use a random Chrome User-Agent
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/",  # Simulate traffic from Google search
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        # Initialize containers for categories and news data
        self.cat_hrefs = list()  # List of category links
        self.cat_dict = dict()  # Mapping of category codes to names
        self.news_hrefs = list()  # List of news links
        self.news_contents = dict()  # Dictionary to store news contents

    @staticmethod
    def get_cat_name(href):
        # Extract the category name from the link
        if href.find('list') != -1:
            return href.replace('https://www.cna.com.tw/list/', '').replace('.aspx', '')
        return href[href.find('news/') + 5:href.find('/202')]

    def fetch_home_page(self, target):
        # Fetch and parse the homepage to extract categories
        response = requests.get(self.base_url, headers=self.headers)
        detected_encoding = chardet.detect(response.content)  # Detect encoding
        response.encoding = detected_encoding['encoding']  # Set detected encoding
        soup = BeautifulSoup(response.content, "html.parser")  # Parse the HTML
        categories = soup.find_all(class_="first-level")  # Find category links

        for cat in categories:
            href = cat.get('href')
            cat_name = cat.text
            # Filter categories based on target and predefined list
            if target and target != cat_name:
                continue
            if any(target_cat in href for target_cat in target_cats) and href not in self.cat_hrefs:
                self.cat_hrefs.append(href)
                self.cat_dict[self.get_cat_name(
                    href).replace('/list/', '')] = cat_name

    def crawl_news(self, link):
        # Fetch and parse a single news article
        self.headers["User-Agent"] = self.ua.chrome  # Update User-Agent
        response = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract category, title, and content
        cat = self.cat_dict[self.get_cat_name(link)]
        self.cat_dict['afe'] = '產經'  # Customize specific category mapping
        title = soup.select("h1 > span")[0].text  # Extract title
        paragraphs = soup.select(".paragraph > p")  # Extract paragraphs
        content = ""
        for p in paragraphs:
            content += p.text + '\n'

        return cat, title, content

    def crawl_news_under_cats(self, cat_count=1, news_count=1):
        # Crawl news articles under selected categories
        if cat_count == 99:  # If 99 is specified, crawl all categories
            cat_count = len(self.cat_hrefs)
        for cat_href in self.cat_hrefs[:cat_count]:
            print(f"Now Scraping: {self.cat_dict[self.get_cat_name(cat_href).replace('/list/', '')]}\n")
            self.headers["User-Agent"] = self.ua.chrome  # Update User-Agent
            print(self.domain + cat_href)
            response = requests.get(self.domain + cat_href, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            news_links = soup.select(".mainList > li > a")  # Extract news links

            self.news_hrefs = list()  # Reset news links for each category
            for news in news_links:
                news_href = news.get('href')
                if news_href.find("https") == -1:  # If the link is relative, make it absolute
                    self.news_hrefs.append(self.domain + news_href)

            for single_news in self.news_hrefs[:news_count]:
                # Crawl each news article and store the result
                cat, title, content = self.crawl_news(single_news)
                try:
                    self.news_contents[cat].append({
                        'url': single_news,
                        'title': title,
                        'content': content
                    })
                except KeyError:
                    # If the category is not yet in `news_contents`, initialize it
                    self.news_contents[cat] = list()
                    self.news_contents[cat].append({
                        'url': single_news,
                        'title': title,
                        'content': content
                    })

    def save_result(self):
        # Save the crawled news data to a JSON file
        with open("cna_news.json", "w", encoding="utf-8") as json_file:
            json.dump(self.news_contents, json_file, ensure_ascii=False, indent=4)
