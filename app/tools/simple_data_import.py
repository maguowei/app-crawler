"""导入测试数据
"""

from app.service.redis_service import DouyinUserBigV, DouyinTopVideo

# 测试数据
uids = ['84990209480', '88445518961', '104255897823', '76055758243', '6556303280', '80812090202']
video_ids = ['6768618740750748936', '6768648652828249355', '6768653399891217668', '6768647119449394435']


if __name__ == '__main__':
    for uid in uids:
        DouyinUserBigV.add(uid, 1)

    for video_id in video_ids:
        DouyinTopVideo.add(video_id, 1)
