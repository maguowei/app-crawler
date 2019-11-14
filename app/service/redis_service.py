import redis
from app import settings


redis_client = redis.Redis(**settings.REDIS)


class DouyinUserZsetBase:
    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    @classmethod
    def add(cls, uid, score):
        """
        :param uid:
        :param score: follow_count
        :return:
        """
        key = cls.get_key()
        redis_client.zadd(key, {uid: score})

    @classmethod
    def exist(cls, uid):
        return redis_client.zscore(cls.get_key(), uid)

    @classmethod
    def nums(cls):
        key = cls.get_key()
        return redis_client.zcard(key)

    @classmethod
    def export(cls):
        for uid in redis_client.zscan_iter(cls.get_key()):
            print(uid)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.nums()}'


class DouyinBase:
    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    @classmethod
    def add(cls, uid):
        key = cls.get_key()
        redis_client.sadd(key, uid)

    @classmethod
    def remove(cls, uid):
        key = cls.get_key()
        redis_client.srem(key, uid)

    @classmethod
    def exist(cls, uid):
        return redis_client.sismember(cls.get_key(), uid)

    @classmethod
    def nums(cls):
        key = cls.get_key()
        return redis_client.scard(key)

    @classmethod
    def export(cls):
        for uid in redis_client.sscan_iter(cls.get_key()):
            print(uid)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.nums()}'


class DouyinUser(DouyinBase):
    """抖音用户池"""
    @classmethod
    def get_key(cls):
        return 'dy:user'


class DouyinUserBigV(DouyinUserZsetBase):
    """抖音大V用户池"""
    @classmethod
    def get_key(cls):
        return 'dy:user:score'


class DouyinUserInfo(DouyinBase):
    """用户信息已抓取"""
    @classmethod
    def get_key(cls):
        return 'dy:user_info'


class DouyinUserFollowing(DouyinBase):
    """已经爬取粉丝的用户"""
    @classmethod
    def get_key(cls):
        return 'dy:user_following'


class DouyinUserFollower(DouyinBase):
    """已经爬取关注的用户"""
    @classmethod
    def get_key(cls):
        return 'dy:user_follower'


class DouyinChallenge(DouyinBase):
    @classmethod
    def get_key(cls):
        return 'dy:challenge'


class DouyinUserErr(DouyinBase):
    """异常用户"""
    @classmethod
    def get_key(cls):
        return 'dy:user_err'


if __name__ == '__main__':
    print(DouyinUser())
    print(DouyinUserBigV())
    print(DouyinUserInfo())
    print(DouyinUserFollower())
    print(DouyinUserFollowing())
    print(DouyinChallenge())
    print(DouyinUserErr())

    # DouyinUserBigV.export()
