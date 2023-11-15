import os
import json
import requests

def get_cat_urls(retry=0):
    if not os.path.exists('data/'):
        os.mkdir('data/')
    url = 'https://shopee.vn/api/v4/pages/get_category_tree'
    response = requests.get(url)
    print(f'[INFO] Fetching {url}')
    if response.status_code != 200:
        if retry == 3:
            print(f'[INFOR] FAILURE')
            return 
        print(f'[INFOR] RETRYING . . . . . . . . . . . . . . .')
        return get_cat_urls(retry+1) 
    
    urls = []
    category_list = response.json()['data']['category_list']
    # Save category.json
    with open('data/category.json', 'w', encoding='utf-8') as f:
        json.dump(category_list, f, ensure_ascii=False)
    
    for category in category_list:
        children = category.get('children')
        if not children:
            continue
        print(f'[INFOR] Category: {category["display_name"]}')
        for child in children:
            cate_url = f'https://shopee.vn/i-cat.{child["parent_catid"]}.{child["catid"]}'
            print(f'[INFO] {cate_url}')
            urls.append(cate_url)
    # Save to file 
    with open('data/cat_urls.txt', 'w', encoding="utf-8") as f:
        f.writelines([url + '\n' for url in urls if url if url.strip()])
    return urls