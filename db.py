import pymongo

from config import Config

client = pymongo.MongoClient(
    Config.MONGO_HOST,
    Config.MONGO_PORT,
    username=Config.MONGO_USER,
    password=Config.MONGO_PASS,
    authSource=Config.MONGO_AUTH_DB,
)
db = client[Config.DB_NAME]