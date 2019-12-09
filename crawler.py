#!/usr/bin/env python3

import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import adbutils
from app.driver.douyin import DouyinDriver


class DeviceManager:
    def __init__(self):
        adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        self.devices = adb.device_list()
        self.drivers = []
        for device in self.devices:
            self.drivers.append(DouyinDriver(device.serial))

    def run(self):
        with ThreadPoolExecutor(max_workers=len(d.drivers)) as executor:
            driver_for_comment = random.choice(d.drivers)
            d.drivers.remove(driver_for_comment)
            future_to_driver = {executor.submit(driver.crawler_users, 1): driver for driver in d.drivers}
            executor.submit(driver_for_comment.crawler_comments)
            for future in as_completed(future_to_driver):
                driver = future_to_driver[future]
                executor.submit(driver.crawler_comments)


if __name__ == '__main__':
    d = DeviceManager()
    d.run()
