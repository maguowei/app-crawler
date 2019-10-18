from app.service.redis_service import redis_client
from app.service.mongo_service import db


def mongo_export():
    uids = db['nearby_videos'].distinct('aweme_id')
    for uid in uids:
        print(uid)


def redis_export():
    uids = []
    for uid in redis_client.sscan_iter('varys:douyin-crawler-user'):
        uids.append(int(uid))

    uids.sort()

    for uid in uids:
        print(uid)


if __name__ == '__main__':
    redis_export()
    # mongo_export()
