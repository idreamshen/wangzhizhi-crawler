import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_username = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_database = os.environ["DB_DATABASE"]

# 初始化数据库连接:
engine = create_engine(f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}")
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)