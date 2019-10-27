import json
import mitmproxy.http
import mitmproxy.proxy.protocol
from app.models.douyin import Document
from app.service.redis_service import DouyinUser


class Events:
    def response(self, flow: mitmproxy.http.HTTPFlow):
        response = flow.response
        content = response.text
        url = flow.request.url
        # print(url)

        # 推荐
        if '/aweme/v1/feed/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for aweme in data['aweme_list']:
                    uid = aweme['author_user_id']
                    DouyinUser.add(uid)
        # 同城
        if '/aweme/v1/nearby/feed/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for aweme in data['aweme_list']:
                    uid = aweme['author_user_id']
                    DouyinUser.add(uid)
        # 关注
        elif '/v2/follow/feed/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for aweme in data['data']:
                    uid = aweme['author_user_id']
                    DouyinUser.add(uid)

        # 粉丝关注列表（可获取少于5000条)
        elif '/aweme/v1/user/follower/list/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for follower in data['followers']:
                    uid = follower['uid']
                    DouyinUser.add(uid)

        # 用户关注列表
        elif '/aweme/v1/user/following/list/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more']:
                for following in data['followings']:
                    uid = following['uid']
                    DouyinUser.add(uid)

        elif '/aweme/v1/user/' in url:
            data = json.loads(content)
            if data['status_code'] == 0:
                user = data['user']
                # db['douyin_user'].replace_one({'uid': user['uid']}, user, upsert=True)

        # 评论列表 (似乎没有限制条数)
        elif '/aweme/v2/comment/list' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for comment in data['comments']:
                    cid = comment['cid']
                    uid = comment['user']['uid']
                    user = comment['user']

                    comment = {
                        'cid': cid,
                        'aweme_id': comment['aweme_id'],
                        'uid': user['uid'],
                        'avatar_url': user['avatar_medium']['url_list'][0],
                        'nickname': user['nickname'],
                        'create_time': comment['create_time'],
                        'text': comment['text'],
                        'digg_count': comment['digg_count'],
                        'reply_id': comment['reply_id'],
                        'user_digged': comment['user_digged'],
                        'reply_comment': comment['reply_comment'],
                        'text_extra': comment['text_extra'],
                        'reply_comment_total': comment['reply_comment_total'],
                        'reply_to_reply_id': comment['reply_to_reply_id'],
                        'is_author_digged': comment['is_author_digged'],
                        'stick_position': comment['stick_position'],
                    }

                    # db['douyin_comment'].replace_one({'cid': cid}, comment, upsert=True)
                    DouyinUser.add(uid)
