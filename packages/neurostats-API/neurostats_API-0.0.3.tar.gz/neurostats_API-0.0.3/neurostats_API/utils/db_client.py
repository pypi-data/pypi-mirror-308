import os
from pymongo import MongoClient
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 創建並共享 MongoClient 連線
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
shared_client = MongoClient(mongo_uri)