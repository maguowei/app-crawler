from sqlalchemy import Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.service.store import engine


Session = sessionmaker(bind=engine)
Base = declarative_base()


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    data = Column(JSON)


# Base.metadata.create_all(engine)
