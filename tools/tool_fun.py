import json

def python_inter(py_code, g=None):
    """
    专门用于执行python代码，并获取最终查询或处理结果。
    :param py_code: 字符串形式的Python代码，
    :param g: g，字典形式变量，表示环境变量，若未提供则创建一个新的字典
    :return：代码运行的最终结果
    """
    if g is None:
        g = {}  # 使用空字典作为默认全局环境

    try:
        # 尝试如果是表达式，则返回表达式运行结果
        return str(eval(py_code, g))
    except Exception as e:
        # 记录执行前的全局变量
        global_vars_before = set(g.keys())
        try:
            exec(py_code, g)
        except Exception as e:
            return f"代码执行时报错: {e}"
        # 记录执行后的全局变量，确定新变量
        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        # 若存在新变量
        if new_vars:
            result = {var: g[var] for var in new_vars}
            return str(result)
        else:
            return "已经顺利执行代码"


def sql_inter(sql_query, host, user, password, database, port):
    """
    用于执行一段SQL代码，并最终获取SQL代码执行结果，
    核心功能是将输入的SQL代码传输至MySQL环境中进行运行，
    并最终返回SQL代码运行结果。需要注意的是，本函数是借助pymysql来连接MySQL数据库。
    :param sql_query: 字符串形式的SQL查询语句，用于执行对MySQL中telco_db数据库中各张表进行查询，并获得各表中的各类相关信息
    :param host: MySQL服务器的主机名
    :param user: MySQL服务器的用户名
    :param password: MySQL服务器的密码
    :param database: MySQL服务器的数据库名
    :param port: MySQL服务器的端口
    :param g: g，字符串形式变量，表示环境变量，无需设置，保持默认参数即可
    :return：sql_query在MySQL中的运行结果。
    """
    from datetime import datetime

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
    # 创建数据库引擎
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    # 创建会话
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()

    try:
        from sqlalchemy import text
        # 执行SQL查询
        result = db_session.execute(text(sql_query))
        results = result.fetchall()

        # # 将结果转换为字典列表
        keys = result.keys()
        results_list = [dict(zip(keys, row)) for row in results]

        # 序列化处理函数
        # 序列化处理函数
        def json_serial(obj):
            """JSON serializer for objects not serializable by default json code"""
            if isinstance(obj, datetime):
                return obj.isoformat()  # 将 datetime 对象转为 ISO 8601 格式的字符串
            raise TypeError("Type not serializable")

        # 返回 JSON 格式的查询结果
        return json.dumps(results_list, default=json_serial)

    finally:
        db_session.close()  # 确保关闭会话

    # 返回 JSON 格式的查询结果

    return "数据库查询出错"