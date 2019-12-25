import time
from app.driver.base import BaseDriver
from app.utils.decorator import retry
from app.models import session
from app.models.douyin import User
from app.service.redis_service import DouyinTopVideo, DouyinUserBigV


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

    def __init__(self, device_serial=None):
        super().__init__(device_serial)
        self.pkg_name = 'com.ss.android.ugc.aweme'
        self.activity = '.main.MainActivity'
        self.popup_list = ['以后再说', '取消', '我知道了', '暂不', '同意', '不允许', '长按屏幕使用更多功能', '确定']
        self.break_list = ['没有更多了', '没有更多了~', 'TA还没有关注任何人', '暂时没有更多了', '该用户还没有发布过作品', '上拉加载更多']
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
        self.open_schema(self.URL_SCHEMA_MAP['detail'].format(aweme_id=aweme_id))

    @retry(10)
    def crawler_users(self, max_num=200):
        """抓取大v用户信息
        """
        while DouyinUserBigV.nums():
            self.app_close()
            self.app_start()
            time.sleep(0.2)
            uid = DouyinUserBigV.pop_min()
            self.crawler_user(uid, max_num=max_num)
            self.app_close()
        else:
            # user import
            pass

    @retry(3)
    def crawler_user(self, uid, max_num=200):
        self.logger.info(f'爬取用户信息: {uid}')
        self.open_user_home(uid)
        time.sleep(0.2)
        self.close_popup()
        # 添加关注
        # self.session(resourceId='com.ss.android.ugc.aweme:id/c6v').click_exists(timeout=1)
        time.sleep(0.1)
        self.session(textContains='作品').click()
        self.do_forever(self.fling, activity='com.ss.android.ugc.aweme.profile.ui.UserProfileActivity', max_num=max_num)
        # self.device.press('back')

    @retry(3)
    def crawler_comments(self):
        while DouyinTopVideo.nums():
            aweme_id, _ = DouyinTopVideo.pop_max()
            self.crawler_comment(aweme_id)

    @retry(3)
    def crawler_comment(self, aweme_id):
        self.app_close()
        self.app_start()
        self.logger.info(f'爬取视频评论: {aweme_id}')
        self.open_video(aweme_id)
        time.sleep(0.2)
        self.close_popup()
        self.session(resourceId="com.ss.android.ugc.aweme:id/v3").click()
        time.sleep(0.2)
        for i in range(150):
            # self.swipe_up()
            self.fling()
            self.logger.info(f'fling: {i}')
            time.sleep(0.1)
            if self.exists(text='暂时没有更多了'):
                break
            # if self.exists(text='暂无评论，来抢沙发'):
            #     break
        self.app_close()

    @retry(10)
    def crawler_following(self):
        """抓取用户关注列表
        """
        time.sleep(2)
        users = session.query(User.uid)
        for user in users:
            uid = user['uid']
            self.logger.info(f'爬取用户关注列表: {uid}')
            self.open_schema(self.URL_SCHEMA_MAP['user'].format(uid=uid))
            time.sleep(0.2)
            if self.session(resourceId="com.ss.android.ugc.aweme:id/bq3").exists:  # 用户昵称
                # if self.session(text='这是私密帐号').exists:  # 跳过私密账号
                #     continue
                self.session(resourceId='com.ss.android.ugc.aweme:id/ah1').click()  # 关注列表按钮
                self.do_forever(self.fling)
            else:
                self.logger.info(f'用户异常: {uid}')
            self.device.press('back')
            time.sleep(0.2)

    @retry(10)
    def crawler_follower(self, max_num=200):
        """抓取用户粉丝列表
        """
        while DouyinUserBigV.nums():
            self.app_close()
            self.app_start()
            time.sleep(0.2)
            uid = DouyinUserBigV.pop_max()
            self.logger.info(f'爬取用户粉丝列表: {uid}')
            self.open_schema(self.URL_SCHEMA_MAP['user'].format(uid=uid))
            time.sleep(0.5)
            if self.session(resourceId='com.ss.android.ugc.aweme:id/ahb').exists:
                self.session(text='粉丝').click()
                time.sleep(0.5)
                self.do_forever(self.fling, activity='com.ss.android.ugc.aweme.following.ui.FollowRelationTabActivity',
                                max_num=max_num)
            else:
                self.logger.info(f'用户异常: {uid}')
            self.app_close()
