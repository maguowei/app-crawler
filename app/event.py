import json
import mitmproxy.http
import mitmproxy.proxy.protocol
from app.service.mongo_service import db
from app.service.redis_service import DouyinCrawlerUser
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
                    aweme_id = aweme['aweme_id']
                    db['douyin_feed_videos'].replace_one({'aweme_id': aweme_id}, aweme, upsert=True)
                    DouyinCrawlerUser.add(aweme['author_user_id'])
        # 同城
        if '/aweme/v1/nearby/feed/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for aweme in data['aweme_list']:
                    uid = aweme['author_user_id']
                    author = aweme['author']
                    user_info = {
                        'uid': uid,
                        'short_id': author['short_id'],
                        'nickname': author['nickname'],
                        'author_avatar': author['avatar_medium']['url_list'][0],
                        'signature': author['signature'],
                        'custom_verify': author['custom_verify'],
                        'school': author['school_name'],
                        'sex': author['gender'],
                        'birthday': author['birthday'],
                        # 'city_cide': aweme['room']['citycode'],
                        'post_count': '',
                        'follow_count': '',
                        'digg_count': '',
                    }
                    db['douyin_nearby_user'].replace_one({'uid': uid}, user_info, upsert=True)
                    DouyinCrawlerUser.add(aweme['author_user_id'])
        # 关注
        elif '/v2/follow/feed/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for aweme in data['data']:
                    aweme_id = aweme['aweme']['aweme_id']
                    db['douyin_follow_videos'].replace_one({'aweme.aweme_id': aweme_id}, aweme, upsert=True)
                    DouyinCrawlerUser.add(aweme['author_user_id'])
        # 粉丝关注列表（可获取少于5000条)
        elif '/aweme/v1/user/follower/list/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more'] == 1:
                for follower in data['followers']:
                    uid = follower['uid']
                    user_info = {
                        'uid': uid,
                        'short_id': follower['short_id'],
                        'unique_id': follower['unique_id'],
                        'nickname': follower['nickname'],
                        'author_avatar': follower['avatar_medium']['url_list'][0],
                        'signature': follower['signature'],
                        'custom_verify': follower['custom_verify'],
                        'school': follower['school_name'],
                        'sex': follower['gender'],
                        'birthday': follower['birthday'],
                        # 'city_cide': aweme['room']['citycode'],
                        'post_count': '',
                        'follow_count': '',
                        'digg_count': '',
                    }
                    db['douyin_follower_users'].replace_one({'uid': uid}, user_info, upsert=True)
                    DouyinCrawlerUser.add(uid)
        # 用户关注列表
        elif '/aweme/v1/user/following/list/' in url:
            data = json.loads(content)
            if data['status_code'] == 0 and data['has_more']:
                for following in data['followings']:
                    uid = following['uid']
                    user_info = {
                        'uid': uid,
                        'short_id': following['short_id'],
                        'unique_id': following['unique_id'],
                        'nickname': following['nickname'],
                        'author_avatar': following['avatar_medium']['url_list'][0],
                        'signature': following['signature'],
                        'custom_verify': following['custom_verify'],
                        'school': following['school_name'],
                        'sex': following['gender'],
                        'birthday': following['birthday'],
                        # 'city_cide': aweme['room']['citycode'],
                        'post_count': '',
                        'follow_count': '',
                        'digg_count': '',
                    }
                    db['douyin_following_users'].replace_one({'uid': uid}, user_info, upsert=True)
                    DouyinCrawlerUser.add(uid)
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
                    user_info = {
                        'uid': uid,
                        'short_id': user['short_id'],
                        'unique_id': user['unique_id'],
                        'nickname': user['nickname'],
                        'author_avatar': user['avatar_medium']['url_list'][0],
                        'signature': user['signature'],
                        'custom_verify': user['custom_verify'],
                        # 'school': user['school_name'],
                        'sex': user['gender'],
                        'birthday': user['birthday'],
                        # 'city_cide': aweme['room']['citycode'],
                        'country': user['country'],
                        'province': user['province'],
                        'location': user['location'],
                        'city': user['city'],
                        'post_count': user['aweme_count'],
                        'follow_count': user['follower_count'],
                        'following_count': user['following_count'],
                        'digg_count': user['total_favorited'],
                        'favoriting_count': user['favoriting_count']
                    }
                    db['douyin_comment'].replace_one({'cid': cid}, comment, upsert=True)
                    db['douyin_comment_user'].replace_one({'uid': uid}, user_info, upsert=True)
                    DouyinCrawlerUser.add(uid)
