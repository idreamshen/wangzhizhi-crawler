from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class City(Base):
    # 表的名字:
    __tablename__ = 'wzz_city'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    name = Column(String(255))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    version = Column(Integer)