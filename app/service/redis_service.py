import redis
from app import settings


redis_client = redis.Redis(**settings.REDIS)


class DouyinZsetBase:
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
    def pop_max(cls):
        values = redis_client.zrevrange(cls.get_key(), 0, 0)
        value = values[0] if values else None
        if value:
            redis_client.zrem(cls.get_key(), value)
        return value

    @classmethod
    def pop_min(cls):
        values = redis_client.zrange(cls.get_key(), 0, 0)
        value = values[0] if values else None
        if value:
            redis_client.zrem(cls.get_key(), value)
        return value

    @classmethod
    def export(cls):
        for uid, score in redis_client.zscan_iter(cls.get_key()):
            print(uid, score)

    def __contains__(self, item):
        value = redis_client.zscore(self.get_key(), item)
        return True if value else False

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
    def pop(cls):
        return redis_client.spop(cls.get_key())

    @classmethod
    def remove(cls, uid):
        key = cls.get_key()
        redis_client.srem(key, uid)

    @classmethod
    def nums(cls):
        key = cls.get_key()
        return redis_client.scard(key)

    @classmethod
    def export(cls):
        for uid in redis_client.sscan_iter(cls.get_key()):
            print(uid)

    def __contains__(self, item):
        return redis_client.sismember(self.get_key(), item)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.nums()}'


class DouyinUser(DouyinBase):
    """待处理抖音用户"""
    @classmethod
    def get_key(cls):
        return 'dy:user'


class DouyinUserBigV(DouyinZsetBase):
    """抖音大V用户池"""
    @classmethod
    def get_key(cls):
        return 'dy:user:score'


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


class DouyinTopVideo(DouyinZsetBase):
    """高赞视频"""
    @classmethod
    def get_key(cls):
        return 'varys:douyin-crawler:video_top'


if __name__ == '__main__':
    print(DouyinUser())
    print(DouyinUserBigV())
    print(DouyinUserFollower())
    print(DouyinUserFollowing())
    print(DouyinTopVideo())
    # DouyinUserBigV.export()
