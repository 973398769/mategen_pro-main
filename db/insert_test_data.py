# -*- coding: utf-8 -*-
"""
Author: MuYu_Cheney
Date: 2024/11/29$
"""



if __name__ == '__main__':
    # 开发环境
    #
    from config.config import SQLALCHEMY_DATABASE_URI, username, password, hostname, database_name

    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    # # 删除所有表
    Base.metadata.drop_all(engine)
    # # # # # 初始化操作
    # initialize_database(username=username,
    #                     password=password,
    #                     hostname=hostname,
    #                     database_name=database_name)

    # from sqlalchemy import create_engine, text
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:snowball950123@192.168.110.131/telco_db?charset=utf8mb4"
    #
    # engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    # import pandas as pd
    #
    # # 使用连接来执行命令
    # # SQL 创建表语句
    # # 使用 text 包装 SQL 创建表语句
    # create_table_statement = text("""
    # CREATE TABLE IF NOT EXISTS user_demographics (
    #     customerID VARCHAR(255) PRIMARY KEY,
    #     gender VARCHAR(255),
    #     SeniorCitizen INT,
    #     Partner VARCHAR(255),
    #     Dependents VARCHAR(255)
    # )
    # """)
    #
    # # 使用连接来执行创建表命令
    # with engine.connect() as conn:
    #     conn.execute(create_table_statement)  # 创建表
    #
    #
    # # 读取 CSV 文件
    # df = pd.read_csv('../user_demographics.csv')
    #
    # df.to_sql('user_demographics', con=engine, index=False, if_exists='append', chunksize=500)
    #
    # # 创建 user_services 表的 SQL 语句
    # create_table_user_services = text("""
    # CREATE TABLE IF NOT EXISTS user_services (
    #     customerID VARCHAR(255) PRIMARY KEY,
    #     PhoneService VARCHAR(255),
    #     MultipleLines VARCHAR(255),
    #     InternetService VARCHAR(255),
    #     OnlineSecurity VARCHAR(255),
    #     OnlineBackup VARCHAR(255),
    #     DeviceProtection VARCHAR(255),
    #     TechSupport VARCHAR(255),
    #     StreamingTV VARCHAR(255),
    #     StreamingMovies VARCHAR(255)
    # )
    # """)
    #
    # # 使用连接来执行创建表命令
    # with engine.connect() as conn:
    #     conn.execute(create_table_user_services)  # 创建表
    #
    # df_services = pd.read_csv('../user_services.csv')  # 确保文件路径正确
    #
    # # 将数据导入到数据库中
    # df_services.to_sql('user_services', con=engine, index=False, if_exists='append', chunksize=500)
    #
    # # 创建 user_payments 表的 SQL 语句
    # create_table_user_payments = text("""
    # CREATE TABLE IF NOT EXISTS user_payments (
    #     customerID VARCHAR(255) PRIMARY KEY,
    #     Contract VARCHAR(255),
    #     PaperlessBilling VARCHAR(255),
    #     PaymentMethod VARCHAR(255),
    #     MonthlyCharges FLOAT,
    #     TotalCharges VARCHAR(255)
    # )
    # """)
    #
    # # 使用连接来执行创建表命令
    # with engine.connect() as conn:
    #     conn.execute(create_table_user_payments)  # 创建表
    #
    # # 读取 CSV 文件
    # df_payments = pd.read_csv('../user_payments.csv')  # 确保文件路径正确
    #
    # # 将数据导入到数据库中
    # df_payments.to_sql('user_payments', con=engine, index=False, if_exists='append', chunksize=500)
    #
    # # 创建 user_churn 表的 SQL 语句
    # create_table_user_churn = text("""
    # CREATE TABLE IF NOT EXISTS user_churn (
    #     customerID VARCHAR(255) PRIMARY KEY,
    #     Churn VARCHAR(255)
    # )
    # """)
    #
    # # 使用连接来执行创建表命令
    # with engine.connect() as conn:
    #     conn.execute(create_table_user_churn)  # 创建表
    #
    # # 读取 CSV 文件
    # df_payments = pd.read_csv('../user_churn.csv')  # 确保文件路径正确
    #
    # # 将数据导入到数据库中
    # df_payments.to_sql('user_churn', con=engine, index=False, if_exists='append', chunksize=500)