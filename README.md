# Thu thập dữ liệu Shopee

## Tổng quan

* Thu thập thông tin các sản phẩm từ sàn thương mại điện tử [shopee](https://shopee.vn/)


* Luồng thu thập dữ liệu
  * Thu thập category (`utils/categor_scraper.py`)
      * Sử dụng api: `https://shopee.vn/api/v4/pages/get_category_tree`
      * Output: data/category.json và data/cat_urls

  * Thu thập product url (`utils/product_url_scraper`)
      * Sử dụng selenium để thu thập product_url
      * Ouput: folder data/product_urls
  
  * Thu thập thông tin chi tiết sản phẩm (`utils/product_url_scraper.py`)
    * Từ product_url, ta lấy được itemid và shopid
    * Sử dụng api `https://shopee.vn/api/v4/pdp/hot_sales/get?item_id=[itemid]&limit=8&offset=0&shop_id=[shopid]`
    * Ouput: dữ liệu được lưu trọng MongoDB

![Luồng thu thập dữ liệu](https://github.com/BigdataCIST/Shopee-Scraper/assets/103992475/cbc45e59-df4e-41c2-9537-be0ba61ab80e)

* Export dữ liệu từ MongoDB ta được 2 file: `data/shopee_products.csv` và `data/shopee_products.xlsx`

## Chạy chương trình
* Tạo file `.env` để lưu trữ thông tin cấu hình MongoDB và `MAX_WORKERS` để chạy đa luồng
* Cài đặt và activate environment
  
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -U webdriver_manager
```

* Chạy chương trình thu thập và biến đổi (transform) dữ liệu sản phẩm
```
python crawl.py
```

* Chạy chương trình export từ dữ liệu ra file csv và excel
```
python export_file.py
```

## Kết quả:
Thực hiện thu thập và biến đổi dữ liệu với `MAX_WORKERS=16` thu được kết quả như sau:

* Tổng số lượng sản phẩm thu thập được: **134,146 sản phẩm**
* Tổng thời gian chạy chương trình: 21715.266s ~  **45.26 phút**
* Tốc độ: **~2963 (sản phẩm/phút)**
