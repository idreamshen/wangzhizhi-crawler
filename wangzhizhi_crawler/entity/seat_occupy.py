from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime, Double
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class SeatOccupy(Base):
    # 表的名字:
    __tablename__ = 'wzz_seat_occupy'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    store_id = Column(Integer)
    seat_id = Column(Integer)
    user_id = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())