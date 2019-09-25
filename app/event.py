import json
from pprint import pprint
import mitmproxy.http
import mitmproxy.proxy.protocol
from app.models.db import db, redis_client
from app.driver.douyin import DouyinDriver


class Events:
    def __init__(self):
        # self.driver = DouyinDriver()
        # self.driver.app_start()
        # self.driver.session(text='同城').click()
        # self.driver.swipe_up()
        pass

    def response(self, flow: mitmproxy.http.HTTPFlow):
        response = flow.response
        content = response.text
        url = flow.request.url
        # print(url)

        # 推荐
        if '/aweme/v1/feed/' in url:
            data = json.loads(content)
            # pprint(data)
            if data['status_code'] == 0 and data['has_more'] == 1:
                # db['nearby'].insert_one(data)
                # db['nearby_videos'].insert_many(data['aweme_list'])
                for aweme in data['aweme_list']:
                    aweme_id = aweme['aweme_id']
                    db['feed_videos'].replace_one({'aweme_id': aweme_id}, aweme, upsert=True)
                    redis_client.sadd('users', aweme['author_user_id'])

        # 同城
        if '/aweme/v1/nearby/feed/' in url:
            data = json.loads(content)
            # pprint(data)
            if data['status_code'] == 0 and data['has_more'] == 1:
                # db['nearby'].insert_one(data)
                # db['nearby_videos'].insert_many(data['aweme_list'])
                for aweme in data['aweme_list']:
                    aweme_id = aweme['aweme_id']
                    db['nearby_videos'].replace_one({'aweme_id': aweme_id}, aweme, upsert=True)
                    redis_client.sadd('users', aweme['author_user_id'])

        # 关注
        elif '/v2/follow/feed/' in url:
            data = json.loads(content)
            # pprint(data)
            db['follow'].insert_one(data)

        # 关注列表
        elif '/aweme/v1/user/follower/list/' in url:
            data = json.loads(content)
            db['followers'].insert_one(data)
            followers = data['followers']
            for follower in followers:
                user = {
                    'uid': follower['uid'],
                    'nickname': follower['nickname'],
                }
                redis_client.sadd('users', user['uid'])
                # print(user)
