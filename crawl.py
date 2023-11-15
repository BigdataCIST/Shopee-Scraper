import re
from glob import glob
from concurrent.futures import ThreadPoolExecutor
from utils.product_scraper import Product
from utils.categor_scraper import get_cat_urls
from utils.product_url_scraper import ProductUrlScraper
from pymongo import MongoClient
from decouple import config
import json
import time

MAX_WORKERS = int(config("MAX_WORKERS"))

# MongoDB 
mongo_client = MongoClient(host=config("MONGO_HOST"),
                           port=int(config("MONGO_PORT")),
                           username=config("MONGO_USER"),
                           password=config("MONGO_PASSWORD"))
col = mongo_client[config("MONGO_DATABASE")][config("MONGO_COLLECTION")]

def list_category_file():
    file_paths = [file_path for file_path in glob('data/product_urls/*.txt')]
    return file_paths

def crawl_product_urls(url):
    """ Crawl product urls using a thread
    """
    bot = ProductUrlScraper(headless=True, category_url=url)
    product_urls = bot.get_product_urls()
    bot.save_product_urls(product_urls)

def crawl_product_detail(path_file):
    """ Crawl product detail using a thread
    """
    cate_ids = re.findall('\d+__\d+', path_file)[0].split('__')
    with open(path_file) as f:
        for url in f:
            url = url.replace('\n', '')
            if not url.strip():
                continue
            bot = Product(url=url, list_category=cate_ids)  
            data = bot.get_product()
            if not data:
                return
            for product in data:
                try:
                    col.insert_one(product)
                except Exception as ex:
                    print(ex)
                    continue

def run_product_url_scraper():
    """ Crawl product urls using multithreads
    """
    category_urls = get_cat_urls()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(crawl_product_urls, category_urls)

def run_product_detail_scraper():
    """ Crawl product detail using multithreads
    """
    file_paths = list_category_file()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(crawl_product_detail, file_paths)

if __name__ == '__main__':
    start_time = time.time()
    print('[INFO] Crawl product urls . . . . . . . . . .')
    run_product_url_scraper()

    print('[INFO] Crawl product detail . . . . . . . . . .')
    run_product_detail_scraper()
    total_time = time.time() - start_time
    
    # Statistic
    ## Total time
    print(f"Total time: {total_time}")
    # Total product
    total_product = col.count_documents({})
    print("Total product: ", total_product)
    # Speed
    print("Speed (product/minute): ", total_product/total_time*60)