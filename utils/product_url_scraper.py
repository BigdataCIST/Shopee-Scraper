import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class ProductUrlScraper:
    def __init__(self, category_url, headless=True, save_path='data/product_urls') -> None:
        options = Options()
        if (headless):
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        self.url = category_url
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print('[INFO] creating product_urls folder')
    
    def get_category_id(self, url):
        category_ids = [token for token in url.split('.') if token.isdigit()]
        return category_ids
    
    def get_product_urls(self):
        print(f"[INFO] Gathering product links from {self.url}")
        self.driver.get(self.url)
        full_urls = []
        try:
            time.sleep(2)
            number_of_page_element = int(self.driver.find_element(By.CSS_SELECTOR, 
                                                        'span.shopee-mini-page-controller__total'))
            number_of_page = number_of_page_element.get_attribute('textContent')
        except Exception as ex:
            print(f'[ERROR] {ex}')
            number_of_page = 9          
        print('[INFO] Number of page: ', number_of_page)
        for i in range(0, number_of_page):
            try:
                time.sleep(2)
                btn_next = self.driver.find_element(By.CSS_SELECTOR, 'a.shopee-button-outline.shopee-mini-page-controller__next-btn')
                self.driver.execute_script("arguments[0].scrollIntoView();", btn_next)
                time.sleep(2)
            except Exception as ex:
                print(ex)
            print('[INFO] Page: ', i, 'of', number_of_page)
            list_product = self.driver.find_elements(By.CSS_SELECTOR, 'ul.row.shopee-search-item-result__items > li')
            for product in list_product:
                try:
                    #scroll to element
                    self.driver.execute_script("arguments[0].scrollIntoView();", product)
                    url = product.find_element(By.CSS_SELECTOR, 'a')
                    url = url.get_attribute('href')
                    print(f'[INFO] {url}')
                    full_urls.append(url)
                except Exception as ex:
                    print(f'[ERROR] {ex}')
            # next page
            try:
                try:
                    btn_next.click()
                except:
                    self.driver.find_element(By.CSS_SELECTOR, 'a.shopee-button-outline.shopee-mini-page-controller__next-btn').click()
            except Exception as ex:
                print(f'[ERROR] {ex}')
                continue

        self.driver.quit()
        return list(set(full_urls))

    def save_product_urls(self, product_urls):
        cate_ids = self.get_category_id(self.url)
        filename = '__'.join(cate_ids)+'.txt'
        with open(os.path.join(self.save_path, filename), "w") as f:
            f.writelines([url+'\n' for url in product_urls if url.strip()])

if __name__ == '__main__':
    with open('data/cat_urls.txt', 'r', encoding='utf-8') as f:
        urls = [url.replace('\n', '') for url in f if url.strip()]
    for url in urls:
        bot = ProductUrlScraper(headless=False, category_url=url)
        product_urls = bot.get_product_urls()
        bot.save_product_urls(product_urls)
