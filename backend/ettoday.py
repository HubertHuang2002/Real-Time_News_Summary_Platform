import requests 
from bs4 import BeautifulSoup 
import random  
import time 
import json  

def crawl_ettoday(article_limit=5, target=""):
    # Define the base URL for ETtoday news
    url = "https://www.ettoday.net/news/news-list.htm"

    # List of User-Agent strings to mimic different devices and browsers
    user_agents = [
        # Windows - Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",

        # Windows - Firefox
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",

        # Windows - Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",

        # MacOS - Chrome
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",

        # MacOS - Safari
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",

        # Linux - Chrome
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",

        # Linux - Firefox
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",

        # Android - Chrome
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",

        # iOS - Safari
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    ]

    # Set request headers with a random User-Agent
    headers = {
        "user-agent": random.choice(user_agents)
    }

    # Send an HTTP GET request to the base URL
    req = requests.get(url, headers=headers)

    # Check the HTTP response status code
    print(f"HTTP status code: {req.status_code}")
    if req.status_code != 200:
        print("Unable to successfully request the target URL")
        return

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(req.text, "lxml")

    # Select the news sections
    segements = soup.select(".part_list_2")
    print(f"Number of extracted news sections: {len(segements)}")

    # Initialize lists to store titles, categories, and links
    title_list = []
    category_list = []
    link_list = []

    # Extract news titles, links, and categories from the selected sections
    for element in segements:
        titles = [title.text.strip() for title in element.select("a")]
        links = [
            i.get('href') if i.get('href').startswith(
                "http") else "https://www.ettoday.net" + i.get('href')
            for i in element.select("a")
        ]
        categories = [category.text.strip()
                      for category in element.select("em")]

        # Extend the lists with extracted data
        title_list.extend(titles)
        link_list.extend(links)
        category_list.extend(categories)

    # Filter by the target category if specified
    if target:
        title_list = [title for title, category in zip(
            title_list, category_list) if category == target]
        link_list = [link for link, category in zip(
            link_list, category_list) if category == target]
        category_list = [
            category for category in category_list if category == target]

    # Limit the number of articles per category
    article = 0
    while article < len(title_list):
        if category_list.count(category_list[article]) > article_limit:
            title_list.pop(article)
            link_list.pop(article)
            category_list.pop(article)
        else:
            article += 1

    # Initialize a dictionary to store the scraped data
    news_dict = {}

    # Loop through the filtered news links to scrape content
    for idx, (link, title, category) in enumerate(zip(link_list, title_list, category_list)):
        try:
            # Send a request to retrieve the news page
            news_resp = requests.get(link, headers=headers)
            news_soup = BeautifulSoup(news_resp.text, "lxml")

            # Extract the content from the news page
            story_div = news_soup.select_one(".story[itemprop='articleBody']")
            if story_div:
                paragraphs = [p.get_text(strip=True)
                              for p in story_div.find_all("p")]
                content = "\n".join(paragraphs)
            else:
                content = "Unable to extract content"

            print(f"Successfully extracted content: {link}")

            # Append the scraped news data into the corresponding category in the dictionary
            if category not in news_dict:
                news_dict[category] = []
            news_dict[category].append({
                "url": link,
                "title": title,
                "content": content
            })

        except Exception as e:
            print(f"Scraping failed, link: {link}, error: {e}")

    # Save the scraped data to a JSON file
    output_file = "ettoday_news.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(news_dict, f, ensure_ascii=False, indent=4)
    print(f"Data has been saved to: {output_file}")