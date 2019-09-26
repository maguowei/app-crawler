import os
import time
from signal import SIGKILL
from app.driver.base import BaseDriver


class DouyinDriver(BaseDriver):

    SEARCH_BUTTON = (0.926, 0.066)

    def __init__(self):
        super().__init__()
        self.pkg_name = 'com.ss.android.ugc.aweme'
        self.activity = '.main.MainActivity'
        self.popup_list = ['以后再说', '取消', '我知道了', '暂不', '同意', '不允许', '长按屏幕使用更多功能']

    def _close_popup(self):
        for text in self.popup_list:
            try:
                self.click_if_exist(text=text)
            except:
                pass

    def crawler_feed(self):
        self.app_start()
        time.sleep(2)
        self.session(text='首页').click()
        self.session(text='推荐').click()
        # self.do_forever(self.swipe_down)
        self.do_forever(self.swipe_down)

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
        self.session(text='首页').click()
        self.session(text='我').click()
        self.session(text='关注').click()
        self.session(text='吴谨言Y').click()
        self.session(text='粉丝').click()
        self.do_forever(self.fling)

    def monitor(self):
        time.sleep(5)
        while True:
            # 检测并关闭弹窗
            self._close_popup()
            # 检测抖音是否关闭
            if not self.is_app_alive():
                # 终止当前进程
                os.kill(os.getpid(), SIGKILL)
