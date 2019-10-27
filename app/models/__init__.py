from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import MYSQL
from sqlalchemy.ext.declarative import as_declarative


engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(**MYSQL), echo=True)

Session = sessionmaker(bind=engine)
session = Session()


@as_declarative()
class Base:
    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()
