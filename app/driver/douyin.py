import time
from app.driver.base import BaseDriver
from app.utils.decorator import retry
from app.service.redis_service import redis_client


class DouyinDriver(BaseDriver):

    SEARCH_BUTTON = (0.926, 0.066)

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

    def open_user_home(self, uid):
        """
        :param uid: 58958068057
        :return:
        """
        self.app_start()
        self.open_schema(self.URL_SCHEMA_MAP['user'].format(uid=uid))
        time.sleep(1)
        self.device.press('back')

    def open_tag(self, cid):
        """

        :param cid: 1643291726734347
        :return:
        """
        self.app_start()
        self.open_schema(self.URL_SCHEMA_MAP['challenge'].format(challenge_id=cid))

    def open_video(self, aweme_id):
        """
        :param aweme_id: 6747930437261298951
        :return:
        """
        self.app_start()
        self.open_schema(self.URL_SCHEMA_MAP['video'].format(aweme_id=aweme_id))

    def crawler_users(self):
        self.app_start()

        for uid in redis_client.sscan_iter('users'):
            print(uid)
            self.open_user_home(uid)
            time.sleep(0.1)

    @retry(10)
    def crawler_feed(self):
        self.app_start()
        time.sleep(2)
        self.session(text='首页').click()
        self.session(text='推荐').click()
        self.do_forever(self.swipe_down)

    @retry(10)
    def crawler_city(self):
        self.app_start()
        time.sleep(2)
        self.session(text='首页').click()
        self.session(text='北京').click()
        self.do_forever(self.swipe_up)

    def crawler_stars(self):
        self.app_start()
        time.sleep(2)
        self.session(text='首页').click()
        self.device.click(*DouyinDriver.SEARCH_BUTTON)
        self.session(text='明星爱DOU榜').click()
        time.sleep(15)
        self.device.click(0.357, 0.287)
        time.sleep(10)
        self.do_forever(self.fling)

    def crawler_follower(self):
        self.app_start()
        time.sleep(2)
        uids = ['84990209480', '88445518961', '104255897823']
        for uid in uids:
            self.open_schema(self.URL_SCHEMA_MAP['user'].format(uid=uid))
            time.sleep(0.2)
            self.session(text='关注').click()
            for i in range(10):
                time.sleep(0.2)
                self.fling()
