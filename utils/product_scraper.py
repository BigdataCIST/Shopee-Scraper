import requests
import redis
from decouple import config
from pymongo import MongoClient

class Product:
    def __init__(self, url, list_category=[]) -> None:
        self.url = url
        self.itemid, self.shopid = self.get_id()
        self.list_category = list_category
        self.headers = {
            'authority': 'shopee.vn',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
            'cache-control': 'max-age=0',
            'cookie': 'SPC_F=3scK28uj6xvCrvleDR7QPx6lGbF1Wqr5; REC_T_ID=aee7cb83-1cdf-11ee-bb89-2cea7f3d8490; SPC_R_T_ID=BTB15JVenfTGBhR0FUWPmJBdo1+KOCi0ZlgdxOTdfE4ufAqbk9boj45VuJqWwac0J9J3N1ywyoQiScHBaVMWDMAf/YkXFwtvUTAiJOI/A1Nse6KzY6cQUc2dZnMiI6Y1/6MyylbfdDC1Sr+CpHAtN0WMcjV0G8ouB14PPzUa+84=; SPC_R_T_IV=dTVtdndoblNEWVJnbFJnZg==; SPC_T_ID=BTB15JVenfTGBhR0FUWPmJBdo1+KOCi0ZlgdxOTdfE4ufAqbk9boj45VuJqWwac0J9J3N1ywyoQiScHBaVMWDMAf/YkXFwtvUTAiJOI/A1Nse6KzY6cQUc2dZnMiI6Y1/6MyylbfdDC1Sr+CpHAtN0WMcjV0G8ouB14PPzUa+84=; SPC_T_IV=dTVtdndoblNEWVJnbFJnZg==; _hjSessionUser_868286=eyJpZCI6IjEyNTM1NzQ4LTA1MzctNTk5Yi04ZjU2LTNkYWM1MDcxZmFmZSIsImNyZWF0ZWQiOjE2ODg3NDU3Njg3MTMsImV4aXN0aW5nIjp0cnVlfQ==; _gcl_au=1.1.488894794.1697378287; csrftoken=YAad2EGHp5a3ioSxuH9GW6GOEywBZrG0; SPC_SI=TasnZQAAAABlbUhTR1JEVupUGQAAAAAAN3p5bUNxdDI=; SPC_SEC_SI=v1-ZzN1cmpZQTZtU1hEbU55ROug7h9OA8FUkXGlMNsbK3FUtP5HegFEOkWkxQ6zD81WPk4gEnxBvIz/JBUGgVYWBNYWOL7WevHP570uio0ILYg=; _QPWSDCXHZQA=715968d3-a6e4-4c66-d565-794986bb48c9; REC7iLP4Q=4033b03d-2c47-4cb3-9516-1133ace2388b; _gid=GA1.2.1522542904.1697378289; shopee_webUnique_ccd=ahImTXs3weOEOvWu4NCcGw%3D%3D%7Ch8Uxbl12Ju9WfJei329wlDlpBpSRcTRaSgvXMx2gjqp72m7KVq%2BDaMg5RC%2F4ju1U%2FVhFAm5GWUo%3D%7CLSejYWdcxIxi%2BfjB%7C08%7C3; ds=9ba0f4aa88e827bdbb524f3dfe32b6d1; _ga_M32T05RVZT=GS1.1.1697378288.3.1.1697379844.52.0.0; _ga=GA1.1.601213259.1688745756; REC_T_ID=7234b489-6b1f-11ee-92b3-c27318b2fa10; SPC_F=kxNXk4eXWaN0nAq0tsrNfACELbjMldo0; SPC_R_T_ID=BTB15JVenfTGBhR0FUWPmJBdo1+KOCi0ZlgdxOTdfE4ufAqbk9boj45VuJqWwac0J9J3N1ywyoQiScHBaVMWDMAf/YkXFwtvUTAiJOI/A1Nse6KzY6cQUc2dZnMiI6Y1/6MyylbfdDC1Sr+CpHAtN0WMcjV0G8ouB14PPzUa+84=; SPC_R_T_IV=dTVtdndoblNEWVJnbFJnZg==; SPC_SEC_SI=v1-dWp1aHVqTFo0OVlIaWZRT4BQ7LHHPQdKu54FMs+nJKh0Z+TIIwCmxannpXa5km3Hh+m1B21SWF7MQjbRq6pOhoXaK9+CuftVbwJle5Km2/0=; SPC_SI=TasnZQAAAABlbUhTR1JEVupUGQAAAAAAN3p5bUNxdDI=; SPC_T_ID=BTB15JVenfTGBhR0FUWPmJBdo1+KOCi0ZlgdxOTdfE4ufAqbk9boj45VuJqWwac0J9J3N1ywyoQiScHBaVMWDMAf/YkXFwtvUTAiJOI/A1Nse6KzY6cQUc2dZnMiI6Y1/6MyylbfdDC1Sr+CpHAtN0WMcjV0G8ouB14PPzUa+84=; SPC_T_IV=dTVtdndoblNEWVJnbFJnZg==',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
            }

    def get_id(self):
        try:
            shopid = int(self.url.split(".")[-2])
            itemid = int(self.url.split(".")[-1].split("?")[0])
            return int(itemid), int(shopid)
        except:
            return None

    def get_product(self):
        # Get api
        api = f"https://shopee.vn/api/v4/pdp/hot_sales/get?item_id={self.itemid}&limit=8&offset=0&shop_id={self.shopid}"
        response = requests.get(api, headers=self.headers)
        if response.status_code != 200:
            print(f'[ERROR] Response status {response.status_code}')
            return None 
        result = response.json()
        if not result.get('data') or not result['data'].get('items'):
            print("[ERROR] Doesn't exist product list")
            return None 
        
        # Get detail
        data = []
        products = result['data'].get('items')
        for product in products:
            item = {}
            item['product_name'] = product['name']
            item['url'] = f"https://shopee.vn/a-i.{product['shopid']}.{product['itemid']}"
            item['product_price'] = product['price_max']/10000
            item['product_revenue'] = product['historical_sold']*item['product_price']
            data.append(item)
        return data