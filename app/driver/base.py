import time
import logging
import uiautomator2 as u2

FORMAT = "[%(process)d-%(filename)s:%(lineno)s - %(funcName)20s %(levelname)s] %(message)s"


class BaseDriver:
    def __init__(self):
        self.device = u2.connect()
        self.session = None
        self.pkg_name = None
        self.activity = None
        self.size = self.device.window_size()
        self.width, self.height = self.size

        # set logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format=FORMAT)
        self.logger.setLevel(logging.DEBUG)

    def app_start(self):
        self.device.app_start(self.pkg_name, self.activity)
        self.session = self.device.session(self.pkg_name, attach=True)

    def size(self):
        self.device.window_size()

    def get_source(self):
        return self.device.dump_hierarchy()

    def get_current_package(self):
        pkg_name = self.device.info.get('currentPackageName')
        return pkg_name

    def do_forever(self, action, *args, **kwargs):
        """TODO 更改为装饰器
        """
        while True:
            self.logger.info('action to do....')
            action(*args, **kwargs)
            # time.sleep(1)
            self.logger.info(f'{action.__name__} action done!')

    def swipe(self, *args):
        self.device.swipe(*args)

    def swipe_right(self, t=0.1, delay=1):
        self.device.swipe(0.1, 0.5, 0.9, 0.5, t)
        time.sleep(delay)

    def swipe_left(self, t=0.1, delay=1):
        self.device.swipe(0.9, 0.5, 0.1, 0.5, t)
        time.sleep(delay)

    def swipe_up(self, t=0.02, delay=0.2):
        self.device.swipe(self.width * 0.8, self.height * 0.8, self.width * 0.8, self.height * 0.1, t)
        time.sleep(delay)

    def swipe_down(self, t=0.02, delay=0.5):
        self.device.swipe(self.width * 0.5, self.height * 0.2, self.width * 0.5, self.height * 0.8, t)
        time.sleep(delay)

    def exists(self, **kwargs):
        return self.device(**kwargs).exists

    def click_if_exist(self, **kwargs):
        d = self.device(**kwargs)
        if d.exists:
            try:
                d.click(timeout=2)
            except Exception as e:
                self.logger.info(e)

    def close_app(self):
        if self.session:
            self.session.close()
        else:
            self.logger.info('Please open_app first')
