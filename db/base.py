# -*- coding: utf-8 -*-
"""
Author: MuYu_Cheney
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from config.config import SQLALCHEMY_DATABASE_URI

# 创建引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=True,
    pool_size=10,  # 设置连接池大小为10
    max_overflow=20  # 最大溢出连接数为20
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

# 创建 Base 类
Base = declarative_base()


# 获取数据库会话
def get_db():
    """
    1. 函数被调用时，它会创建一个数据库会话 db = SessionLocal()。
    2. 程序暂停执行，yield db 将会话对象 db 返回给调用者，调用者可以通过这个对象与数据库交互。
    3. 数据库交互操作完成后，控制权回到 finally 语句块，调用 db.close() 关闭数据库会话，释放连接资源。
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        db.rollback()  # 如果发生错误，回滚事务
    finally:
        db.close()
