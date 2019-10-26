# app crawler

crawling app by uiautomator2 &amp; mitmproxy

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

# 抖音安装

- 使用豌豆荚安装旧版抖音APP(v7.5.0以下版本仍然信任用户CA证书)

## mitmproxy

### 安装和信任证书
- https://docs.mitmproxy.org/stable/concepts-certificates/

### 启动
```bash
make run
dy.py crawler_feed
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
