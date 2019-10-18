import redis
from app import settings


redis_client = redis.Redis(**settings.REDIS['varys'])


class DouyinCrawlerUser:
    @classmethod
    def get_key(cls):
        return f'varys:douyin-crawler-user'
    @classmethod
    def add(cls, uid):
        key = cls.get_key()
        redis_client.sadd(key, uid)
    @classmethod
    def user_nums(cls):
        key = cls.get_key()
        return redis_client.scard(key)


if __name__ == '__main__':
    print(DouyinCrawlerUser.user_nums())