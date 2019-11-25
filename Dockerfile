FROM maguowei/python-app:onbuild
ENV APP_NAME app-crawler
ENV APP_ENV dev
COPY --chown=app:app .mitmproxy /home/app/.mitmproxy
CMD mitmdump -s manage.py
