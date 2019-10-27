from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import MYSQL


engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(**MYSQL), echo=True)

Session = sessionmaker(bind=engine)
session = Session()
