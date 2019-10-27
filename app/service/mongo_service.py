from pymongo import MongoClient
import pymongo
from app import settings
from app.service.redis_service import redis_client, DouyinUserBigV


client = MongoClient(settings.MONGODB_URI)
db = client['douyin_user']


class MongoService:
    @classmethod
    def get_top_videos(cls, num=1000):
        videos = db['feed_videos'].find({}, ['author.uid', 'author.nickname', 'statistics.digg_count']).sort('statistics.digg_count', pymongo.DESCENDING).limit(num)
        return videos

    @classmethod
    def get_top_users(cls, num=10000):
        users = db['douyin_user'].find({'follower_count': {'$gt': 500000}}, ['uid', 'nickname', 'follower_count']).sort(
            'follower_count', pymongo.DESCENDING).limit(num)
        return users

    @classmethod
    def mongo_uid_export(cls):
        users = cls.get_top_users()
        for user in users:
            # print(user)
            redis_client.sadd('top_users', user['uid'])


if __name__ == '__main__':
    # videos = MongoService.get_top_videos()
    # for v in videos:
    #     print(v)
    users = MongoService.get_top_users(10000)
    for user in users:
        print(user)
        # print(user['uid'], user['follower_count'])
        # DouyinUserBigV.add(user['uid'], user['follower_count'])
