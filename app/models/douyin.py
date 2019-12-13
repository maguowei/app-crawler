import datetime
from sqlalchemy import Column, Integer, JSON, String, Boolean, DateTime, SMALLINT
from app.models import engine
from app.models import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    uid = Column(String(50), index=True)
    short_id = Column(String(50), nullable=False, default='')
    unique_id = Column(String(50), nullable=False, default='')
    nickname = Column(String(50), nullable=False, default='')
    signature = Column(String(200), nullable=False, default='')
    custom_verify = Column(String(200), nullable=False, default='')
    gender = Column(SMALLINT, nullable=False, default=0)   # 0 未知, 1 男, 2 女
    school_name = Column(String(50), nullable=False, default='')
    avatar_uri = Column(String(100), nullable=False, default='')
    share_qrcode_uri = Column(String(100), nullable=False, default='')
    birthday = Column(String(100), nullable=False, default='')
    region = Column(String(50), nullable=False, default='')
    country = Column(String(20), nullable=False, default='')
    province = Column(String(20), nullable=False, default='')
    city = Column(String(50), nullable=False, default='')
    is_verified = Column(Boolean, default=False)
    verify_info = Column(String(100), nullable=False, default='')
    is_star = Column(Boolean, default=False)
    room_id = Column(String(50), nullable=False, default='')
    aweme_count = Column(Integer, index=True)
    following_count = Column(Integer, index=True)
    favoriting_count = Column(Integer, index=True)
    total_favorited = Column(Integer, index=True)
    dongtai_count = Column(Integer, index=True)
    follower_count = Column(Integer, index=True)
    is_gov_media_vip = Column(Boolean, default=False)
    followers_detail = Column(JSON)
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


# Base.metadata.create_all(engine)
