from concurrent.futures import ThreadPoolExecutor
import tempfile
import time
from urllib.parse import urljoin
from flask import Flask, Response, request, jsonify
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)

SCRAPER_API_KEY = '2dd1ebf22e3a3d6fbc5435a3d7f46eb5'
MAX_WORKERS = 5  # Numero di thread da usare
MAX_RETRIES = 5  # Numero massimo di tentativi

articles_text = ""

def get_article_text(article_url):
    scraper_api_url = f'http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={article_url}'
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(scraper_api_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.select('div.article__body p')
                text = ' '.join(paragraph.text.strip() for paragraph in paragraphs)
                return text
            elif response.status_code == 429:
                retries += 1
                print(f"Rate limited. Retrying in {2 ** retries} seconds...")
                time.sleep(2 ** retries)
            else:
                print(f"Failed to retrieve the article URL, status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception occurred while retrieving article: {e}")
            return None
    return None

def fetch_article_text(url):
    return get_article_text(url)

def fetch_and_store_articles():
    global articles_text
    url = 'https://www.marketwatch.com/'
    scraper_api_url = f'http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}'
    
    try:
        response = requests.get(scraper_api_url)
        if response.status_code != 200:
            print(f"Failed to retrieve the URL, status code: {response.status_code}")
            return
    except Exception as e:
        print(f"Exception occurred: {e}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    article_urls = []
    for article in soup.select('div.element--article'):
        url_element = article.select_one('a')
        article_url = url_element['href'] if url_element else None
        if article_url and "video" not in article_url:
            article_url = article_url if article_url.startswith('http') else urljoin('https://www.marketwatch.com', article_url)
            article_urls.append(article_url)
    
    articles_texts = []
    for article_url in article_urls:
        text = fetch_article_text(article_url)
        if text:
            articles_texts.append(text)
    
    articles_text = "\n\n".join(articles_texts)

@app.route('/articles', methods=['GET'])
def get_articles():
    global articles_text
    return Response(articles_text, mimetype='text/plain')

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store_articles, 'interval', days=1)
    scheduler.start()
    
    # Esegui fetch_and_store_articles al primo avvio
    fetch_and_store_articles()

    try:
        app.run(debug=True, use_reloader=False, host='0.0.0.0')
    finally:
        scheduler.shutdown()