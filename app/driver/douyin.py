import time
from app.driver.base import BaseDriver
from app.utils.decorator import retry
from app.service.redis_service import DouyinUser, DouyinUserFollowing, DouyinUserFollower, \
    DouyinUserErr, DouyinUserInfo, DouyinUserBigV
from app.service.store import db
from app.service.redis_service import redis_client


class DouyinDriver(BaseDriver):

    # https://s3.pstatp.com/ies/resource/falcon/douyin_falcon/pkg/common_4276a6c.js
    URL_SCHEMA_MAP = {
        'home': "snssdk1128://feed?refer=web",
        'user': 'snssdk1128://user/profile/{uid}?refer=web',
        'detail': 'snssdk1128://aweme/detail/{aweme_id}?refer=web',
        'challenge': 'snssdk1128://challenge/detail/{challenge_id}?refer=web',
        'music': 'snssdk1128://music/detail/{music_id}?refer=web',
        'live': 'snssdk1128://live?room_id={room_id}&user_id={user_id}&from=webview&refer=web',
        'poi":': 'snssdk1128://poi/?id={poi_id}',
        'webview': 'snssdk1128://webview?url={url}&from=webview&refer=web',
        'webview_fullscreen': 'snssdk1128://webview?url={url}&from=webview&hide_nav_bar=1&refer=web',
        'poidetail': 'snssdk1128://poi/detail?id={id}&from=webview&refer=web',
        'forward': 'snssdk1128://forward/detail/{id}',
        'billboard_word': 'snssdk1128://search/trending',
        'billboard_video': "snssdk1128://search/trending?type=1",
        'billboard_music': "snssdk1128://search/trending?type=2",
        'billboard_positive': "snssdk1128://search/trending?type=3",
        'billboard_star': "snssdk1128://search/trending?type=4",
    }

    def __init__(self):
        super().__init__()
        self.pkg_name = 'com.ss.android.ugc.aweme'
        self.activity = '.main.MainActivity'
        self.popup_list = ['以后再说', '取消', '我知道了', '暂不', '同意', '不允许', '长按屏幕使用更多功能', '确定']
        self.app_start()

    def open_user_home(self, uid):
        """
        :param uid: 58958068057
        :return:
        """
        self.open_schema(self.URL_SCHEMA_MAP['user'].format(uid=uid))

    def open_tag(self, cid):
        """

        :param cid: 1643291726734347
        :return:
        """
        self.open_schema(self.URL_SCHEMA_MAP['challenge'].format(challenge_id=cid))

    def open_video(self, aweme_id):
        """
        :param aweme_id: 6747930437261298951
        :return:
        """
        self.open_schema(self.URL_SCHEMA_MAP['video'].format(aweme_id=aweme_id))

    @retry(10)
    def crawler_users(self):
        """抓取用户池用户信息
        """
        self.app_start()

        for uid in redis_client.sscan_iter(DouyinUser.get_key()):
            self.crawler_user(uid)

    @retry(10)
    def crawler_bigv_users(self):
        """抓取大v用户信息
        """
        for uid, _ in redis_client.zscan_iter(DouyinUserBigV.get_key()):
            self.crawler_user(uid)

    @retry(3)
    def crawler_user(self, uid):
        self.logger.info(f'爬取用户信息: {uid}')
        self.open_user_home(uid)
        time.sleep(0.1)
        self.device.press('back')
        redis_client.smove(DouyinUser.get_key(), DouyinUserInfo.get_key(), uid)

    @retry(10)
    def crawler_feed(self):
        time.sleep(2)
        self.session(text='首页').click()
        self.session(text='推荐').click()
        self.do_forever(self.swipe_down)

    @retry(10)
    def crawler_city(self):
        time.sleep(2)
        self.session(text='首页').click()
        self.session(text='北京').click()
        self.do_forever(self.swipe_up)

    @retry(10)
    def crawler_follower(self):
        """抓取用户关注列表
        """
        time.sleep(2)
        users = db['scraped_data_douyin_user_info'].find()
        for user in users:
            uid = user['uid']
            if not (DouyinUserFollower.exist(uid) or DouyinUserErr.exist(uid)):
                self.logger.info(f'爬取用户关注列表: {uid}')
                self.open_schema(self.URL_SCHEMA_MAP['user'].format(uid=uid))
                time.sleep(0.2)
                if self.session(resourceId="com.ss.android.ugc.aweme:id/bq3").exists:  # 用户昵称
                    # if self.session(text='这是私密帐号').exists:  # 跳过私密账号
                    #     continue
                    self.session(resourceId='com.ss.android.ugc.aweme:id/ah1').click()  # 关注列表按钮
                    self.do_forever(self.fling)
                    DouyinUserFollower.add(uid)
                else:
                    self.logger.info(f'用户异常: {uid}')
                    DouyinUserErr.add(uid)
                self.device.press('back')
                time.sleep(0.2)
            else:
                self.logger.info(f'用户关注已经爬取: {uid}')

    @retry(10)
    def crawler_following(self):
        """抓取用户粉丝列表
        """
        time.sleep(2)
        users = db['scraped_data_douyin_user_info'].find()
        for user in users:
            uid = user['uid']
            if not (DouyinUserFollower.exist(uid) or DouyinUserErr.exist(uid)):
                self.logger.info(f'爬取用户粉丝列表: {uid}')
                self.open_schema(self.URL_SCHEMA_MAP['user'].format(uid=uid))
                time.sleep(0.5)
                if self.session(resourceId="com.ss.android.ugc.aweme:id/bq3").exists:
                    self.session(text='粉丝').click()
                    time.sleep(0.5)
                    self.do_forever(self.fling)
                    DouyinUserFollowing.add(uid)
                else:
                    self.logger.info(f'用户异常: {uid}')
            else:
                self.logger.info(f'用户粉丝已经爬取: {uid}')

