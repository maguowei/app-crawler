import os
import time
from signal import SIGKILL
from app.driver.base import BaseDriver


class DouyinDriver(BaseDriver):
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

    def run(self):
        self.app_start()
        time.sleep(2)
        self.session(text='首页').click()
        self.session(text='推荐').click()
        self.do_forever(self.swipe_up)

    def monitor(self):
        time.sleep(5)
        while True:
            # 检测并关闭弹窗
            self._close_popup()
            # 检测抖音是否关闭
            if not self._is_douyin_alive():
                # 终止当前进程
                os.kill(os.getpid(), SIGKILL)

    def _is_douyin_alive(self):
        if self.get_current_package() != self.pkg_name:
            self.logger.info('抖音已经退出')
            return False
        else:
            return True
