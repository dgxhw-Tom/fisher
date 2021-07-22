from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

from app.models.base import db, Base


class Book(Base):
    # primary_key 主键； autoincrement 自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # nullable 是否允许为null
    title = Column(String(50), nullable=False)
    # default 默认值
    author = Column(String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    # unique 参数为该列值必须是唯一的
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
