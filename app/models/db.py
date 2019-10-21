import redis
import pymongo
from pymongo import MongoClient
from app import settings

client = MongoClient(settings.MONGODB_URI)
db = client['douyin']


redis_client = redis.Redis(host=settings.REDIS['HOST'], port=settings.REDIS['PORT'],
                           db=settings.REDIS['DATABASE'], decode_responses=True)


def get_top_videos(num=1000):
    videos = db['feed_videos'].find({}, ['author.uid', 'author.nickname', 'statistics.digg_count']).sort('statistics.digg_count', pymongo.DESCENDING).limit(num)
    return videos


if __name__ == '__main__':
    videos = get_top_videos()
    for v in videos:
        print(v)
