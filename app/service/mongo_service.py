from pymongo import MongoClient
import pymongo
from app import settings
client = MongoClient(settings.MONGODB_URI)
db = client['dm_spider_dev']


class MongoService:
    @classmethod
    def get_top_videos(cls, num=1000):
        videos = db['feed_videos'].find({}, ['author.uid', 'author.nickname', 'statistics.digg_count']).sort('statistics.digg_count', pymongo.DESCENDING).limit(num)
        return videos


if __name__ == '__main__':
    videos = MongoService.get_top_videos()
    for v in videos:
        print(v)
