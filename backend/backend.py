from flask import Flask, request, jsonify
from flask_cors import CORS
import concurrent.futures
import json
import datetime
from cna import crawl_cna  # Function for crawling CNA news
from ettoday import crawl_ettoday  # Function for crawling ETtoday news
from api import get_summary  # Function for generating article summaries

# Initialize the Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Global variables for storing news data and fetch times
news_data = {}
fetch_time = {}

# Function to load news data for a specific category
def load_news(target=""):
    global news_data
    # Crawl news data from ETtoday and CNA based on the target category
    crawl_ettoday(target=target)
    crawl_cna(target=target)

    # Load ETtoday news data from the JSON file
    with open('./ettoday_news.json', 'r', encoding='utf-8') as f:
        additional_news_data = json.load(f)
        for key, value in additional_news_data.items():
            news_data[key] = value

    # Load CNA news data from the JSON file
    with open('./cna_news.json', 'r', encoding='utf-8') as f:
        additional_news_data = json.load(f)
        for key, value in additional_news_data.items():
            # Merge data if the category already exists in `news_data`
            if key in news_data:
                news_data[key].extend(value)
            else:
                news_data[key] = value

    # Generate summaries for all articles in the target category concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            results = list(
                executor.map(
                    get_summary, 
                    [news['url'] for news in news_data[target]],  # URLs of news articles
                    [news['title'] for news in news_data[target]],  # Titles of news articles
                    [news['content'] for news in news_data[target]]  # Content of news articles
                )
            )
        except Exception:
            return

    # Update news data with the summarized title and content
    for result in results:
        url, title, article = result
        for news in news_data[target]:
            if news['url'] == url:
                news['title'] = title
                news['content'] = article
                break

# API route to get news data
@app.route('/api/news', methods=['GET'])
def get_news():
    # Get the category parameter from the request
    category = request.args.get('category')
    global news_data, fetch_time

    # Attempt to load existing data and fetch time from JSON files
    try:
        with open('./news_data.json', 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        with open('./fetch_time.json', 'r', encoding='utf-8') as f:
            fetch_time = json.load(f)
    except Exception:
        pass

    # Check if data for the category was fetched within the last hour
    if category in fetch_time and datetime.datetime.strptime(fetch_time[category], '%Y-%m-%d %H:%M:%S') > datetime.datetime.now() - datetime.timedelta(hours=1):
        print('data passed')
        return jsonify(news_data[category])  # Return cached data
    else:
        # Reload the news data for the category
        load_news(category)
        if category in news_data:
            # Save updated news data and fetch time to JSON files
            with open('./news_data.json', 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=4)
            fetch_time[category] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('./fetch_time.json', 'w', encoding='utf-8') as f:
                json.dump(fetch_time, f, ensure_ascii=False, indent=4)
            print('data passed')
            return jsonify(news_data[category])  # Return updated data
        else:
            # If the category is not found, return an error response
            print('data passed')
            return jsonify({"error": "Category not found"}), 404

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)