# app crawler

crawling app by uiautomator2 &amp; mitmproxy

- [uiautomator2](https://github.com/openatx/uiautomator2)
- [浅谈自动化测试工具 python-uiautomator2](https://testerhome.com/topics/11357)

## 依赖安装

```bash
pipenv install
pipenv shell
uiautomator2 init
```

## mitmproxy

### 安装和信任证书

- https://docs.mitmproxy.org/stable/concepts-certificates/

### 启动

```bash
make run
```

## 查看爬取到的数据

http://127.0.0.1:8081/
