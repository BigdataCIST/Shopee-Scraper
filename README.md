# Thu thập dữ liệu Shopee

## Tổng quan

* Thu thập thông tin các sản phẩm từ sàn thương mại điện tử [shopee](https://shopee.vn/)


* Luồng thu thập dữ liệu

![Luồng thu thập dữ liệu](https://gitlab.com/ManhLk/shopee-scraper/-/raw/dev/figures/Shopee-Scraper.png)

## Chạy chương trình
* Cấu hình số thread crawl thông qua `MAX_WORKERS` trong `config.py`

* Cài đặt và activate environment
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -U webdriver_manager
```

* Chạy chương trình thu thập dữ liệu sản phẩm
```
python main.py
```

* Chạy chương trình thu thập dữ liệu hình ảnh
```
python image_scraper.py
```