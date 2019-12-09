import json
import mitmproxy.http
import mitmproxy.proxy.protocol
from app.models.douyin import User
from app.service.redis_service import DouyinUser


class Events:
    def response(self, flow: mitmproxy.http.HTTPFlow):
        response = flow.response
        content = response.text
        url = flow.request.url
        # print(url)

        # 粉丝关注列表（可获取少于5000条)
        if '/aweme/v1/user/follower/list/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for follower in data['followers']:
                    uid = follower['uid']
                    # DouyinUser.add(uid)

        # 用户关注列表
        elif '/aweme/v1/user/following/list/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more']:
                for following in data['followings']:
                    uid = following['uid']
                    # DouyinUser.add(uid)

        # 用户信息
        elif '/aweme/v1/user/' in url:
            data = json.loads(content)
            if data['status_code'] == 0:
                user = data['user']
                data = {
                    'uid': user['uid'],
                    'short_id': user['short_id'],
                    'unique_id': user['unique_id'],
                    'nickname': user['nickname'],
                    'signature': user['signature'],
                    'custom_verify': user['custom_verify'],
                    'gender': user['gender'],
                    'school_name': user.get('school_name', ''),
                    'avatar_uri': user['avatar_uri'],
                    'share_qrcode_uri': user['share_qrcode_uri'],
                    'birthday': user['birthday'],
                    'region': user['region'],
                    'country': user['country'],
                    'province': user['province'],
                    'city': user['city'],
                    'is_verified': user['is_verified'],
                    'verify_info': user['verify_info'],
                    'is_star': user['is_star'],
                    'room_id': user['room_id'],
                    'aweme_count': user['aweme_count'],
                    'following_count': user['following_count'],
                    'favoriting_count': user['favoriting_count'],
                    'total_favorited': user['total_favorited'],
                    'dongtai_count': user['dongtai_count'],
                    'follower_count': user['follower_count'],
                    'is_gov_media_vip': user['is_gov_media_vip'],
                    'followers_detail': user['followers_detail'],
                }
                User(**data).save()

        # 用户视频列表
        elif '/aweme/v1/aweme/post/' in url:
            if content:
                data = json.loads(content)
                if data['status_code'] == 0:
                    aweme_list = data['aweme_list']
                    for detail in aweme_list:
                        pass
            else:
                print('返回空')

        # 评论列表 (似乎没有限制条数)
        elif '/aweme/v2/comment/list' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for comment in data['comments']:
                    cid = comment['cid']
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
                    }

