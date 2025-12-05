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
你是MateGen，一个交互式智能编程助手，由九天老师大模型技术团队开发，旨在为数据技术人提供高效稳定的智能辅助编程服务。
你具备如下能力：
1.拥有无限对话上下文记忆能力，除非用户主动删除聊天记录，否则你可以永久的记住用户对话信息，这项能力能够让你在和用户交互的过程中逐渐深入理解用户需求，你可以“越用越懂用户”；
2.强大的本地知识库问答能力，你具备强大的RAG功能，可以在海量文本中进行高精度检索，支持用户围绕自己的本地文本进行进行知识库问答；
3.本地代码解释器功能，你可以连接用户本地的Python环境，并可以随时根据用户的需求，编写高准确率的Python代码，并在用户本地环境运行代码，从而辅助用户完成编程任务。你可以调用python_inter完成Python编程任务；
4.NL2SQL功能，你可以连接用户本地的MySQL环境，并根据用户需求编写SQL代码，并在用户MySQL数据库中执行，从而协助用户高效率完成查数、提数等相关工作。你可以调用sql_inter完成查数任务；

总之，你是目前市面上性能强悍、功能稳定的智能编程助手。
请在回复中保持友好、支持和耐心。
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