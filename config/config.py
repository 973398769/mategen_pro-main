import logging
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


# 获取项目的根目录路径
base_path = os.path.dirname(os.path.abspath(__file__))


def setup_logging():
    """
    格式化服务实时日志信息
    :return:
    """
    # 创建一个logger
    logger = logging.getLogger()

    # 设置日志级别为INFO
    logger.setLevel(logging.INFO)

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # 创建一个handler，用于写入日志文件
    log_file_path = os.path.join(base_path, 'mategen_runtime.log')
    file_handler = logging.FileHandler(log_file_path)  # 使用完整路径指定日志文件名
    file_handler.setFormatter(formatter)  # 设置日志格式

    # 创建一个handler，用于将日志输出到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


username = 'root'
database_name = 'mategen'
password = "snowball2019"

# 检查环境变量USE_DOCKER，若不存在或为False，则使用相对路径挂载静态文件
if os.getenv("USE_DOCKER") == "True":
    hostname = 'db'  # Docker环境
else:
    hostname = 'localhost'  # 个人环境开发配置


SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{hostname}/{database_name}?charset=utf8mb4"

assistant_instructions = """
You are MateGen, an interactive coding assistant designed to provide reliable, high-quality support for data practitioners.
Capabilities:
1. Persistent conversation memory (until the user clears history), enabling deeper understanding over time.
2. RAG-based local knowledge-base Q&A: high-accuracy retrieval over large text corpora; supports user-provided documents.
3. Local Python code interpreter: connect to the user's Python environment, author accurate code, and run locally to assist analysis and development. You can call python_inter to run Python code.
4. NL2SQL: connect to the user's local MySQL, write and execute SQL to support data querying tasks. You can call sql_inter to run queries.

Please respond in a friendly, supportive, and patient manner.
"""


if __name__ == '__main__':
    # 创建数据库连接字符串（不包含数据库名）
    SQLALCHEMY_DATABASE_URI_TEST = f"mysql+pymysql://{username}:{password}@{hostname}/"
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI_TEST)

        # 尝试连接到数据库
        with engine.connect() as connection:
            print("数据库连接成功 !")

    except OperationalError as e:
        # 捕获数据库连接错误
        print(f"连接数据库出错: {e}")
    except Exception as e:
        # 捕获其他类型的错误
        print(f"发生意外错误: {e}")