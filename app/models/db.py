import redis
from pymongo import MongoClient
from app import settings

client = MongoClient(settings.MONGODB_URI)
db = client['douyin']


redis_client = redis.Redis(host=settings.REDIS['HOST'], port=settings.REDIS['PORT'],
                           db=settings.REDIS['DATABASE'], decode_responses=True)
