from pymongo import MongoClient
from decouple import config
import pandas as pd

# MongoDB 
mongo_client = MongoClient(host=config("MONGO_HOST"),
                           port=int(config("MONGO_PORT")),
                           username=config("MONGO_USER"),
                           password=config("MONGO_PASSWORD"))
col = mongo_client[config("MONGO_DATABASE")][config("MONGO_COLLECTION")]

cursor = col.find({}, {'_id': 0})
df = pd.DataFrame(list(cursor))
df.to_csv('data/shopee_products.csv', index=False)
# Export to excel
df = df.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
df.to_excel('data/shopee_products.xlsx', index=False, engine='openpyxl')