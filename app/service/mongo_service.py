from pymongo import MongoClient
import pymongo
from app import settings
from app.service.redis_service import redis_client

client = MongoClient(settings.MONGODB_URI)
db = client['douyin_user']


class MongoService:
    @classmethod
    def get_top_videos(cls, num=1000):
        videos = db['feed_videos'].find({}, ['author.uid', 'author.nickname', 'statistics.digg_count']).sort('statistics.digg_count', pymongo.DESCENDING).limit(num)
        return videos

    @classmethod
    def get_top_users(cls, num=1000):
        users = db['douyin_user'].find({}, ['uid', 'nickname', 'follower_count']).sort(
            'follower_count', pymongo.DESCENDING).limit(num)
        return users

    @classmethod
    def mongo_export(cls):
        uids = db['nearby_videos'].distinct('aweme_id')
        for uid in uids:
            print(uid)

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
    MongoService.mongo_uid_export()
