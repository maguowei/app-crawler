import redis
from app import settings


redis_client = redis.Redis(**settings.REDIS)


class DouyinCrawlerUser:
    @classmethod
    def get_key(cls):
        return f'users'

    @classmethod
    def add(cls, uid):
        key = cls.get_key()
        redis_client.sadd(key, uid)

    @classmethod
    def user_nums(cls):
        key = cls.get_key()
        return redis_client.scard(key)

    @classmethod
    def user_export(cls):
        key = cls.get_key()
        uids = []
        for uid in redis_client.sscan_iter(key):
            uids.append(int(uid))

        uids.sort()

        for uid in uids:
            print(uid)

    @classmethod
    def diff(cls):
        uids = redis_client.sdiff('users', 'top_users')
        print(len(uids))


if __name__ == '__main__':
    # print(DouyinCrawlerUser.user_nums())
    DouyinCrawlerUser.diff()
