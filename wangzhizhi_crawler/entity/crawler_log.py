from sqlalchemy.sql import func
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class CrawlerLog(Base):
    # 表的名字:
    __tablename__ = 'wzz_crawler_log'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    crawler_type = Column(String)
    request_url = Column(String)
    response_body = Column(String)
    created_at = Column(DateTime, default=func.now())