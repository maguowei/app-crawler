# app crawler

crawling app by uiautomator2 &amp; mitmproxy

使用 URL_SCHEMA 跳转实现抖音用户视频和视频评论的抓取

```python3
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
```

- [uiautomator2](https://github.com/openatx/uiautomator2)
- [浅谈自动化测试工具 python-uiautomator2](https://testerhome.com/topics/11357)

## 依赖安装

下载 Android platform-tools 并解压获取 `adb`
- https://developer.android.com/studio/releases/platform-tools?hl=zh-Cn

```bash
# 列出连接的设备(设备需开启`开发者选项`）
adb devices
```

- [Android 调试桥 (adb)](https://developer.android.com/studio/command-line/adb?hl=zh-Cn)

```bash
pipenv install
pipenv shell
uiautomator2 init
```

## 抖音安装

- 使用豌豆荚安装旧版抖音APP(v7.5.0以下版本仍然信任用户CA证书)

## weditor

使用web界面查看和定位元素
```bash
python -m weditor

```

## mitmproxy

### 安装和信任证书
- https://docs.mitmproxy.org/stable/concepts-certificates/

### 本地启动
```bash
cp .env.tpl .env
cp -r .mitmproxy ~/.mitmproxy
make run-mitmproxy
./crawler.py
```

### 部署机器进程管理

```bash
sudo cp frp/systemd/app-crawler.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start app-crawler.service

# 重启服务进程
sudo systemctl restart app-crawler.service

# 开机自启动
sudo systemctl enable app-crawler.service
```

## 查看爬取到的数据
http://127.0.0.1:8081/

### 常见问题

1. 找不到设备

```bash
adb kill-server
adb start-server
```
还是不行，重启手机试试

2. `adb devices` 出现 `no permissions (user in plugdev group; are your udev rules wrong?)`
- [adb-devices-no-permissions-user-in-plugdev-group-are-your-udev-rules-wrong](https://stackoverflow.com/questions/53887322/adb-devices-no-permissions-user-in-plugdev-group-are-your-udev-rules-wrong)

3. `weditor` 打开时出现 `adbutils.errors.AdbError: device not found`
更换设备会出现，需要清理 Chrome 的 LocalStorage
- [openatx/weditor/issues/57](https://github.com/openatx/weditor/issues/57)

4. 测试机型

- Xiaomi Mi 6
- Redmi Note 8
