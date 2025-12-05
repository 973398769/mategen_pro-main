from typing_extensions import override
from openai import AssistantEventHandler
import json

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        """响应回复创建事件"""
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        """响应输出生成的流片段"""
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        """响应工具调用"""
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_tool_call_delta(self, delta, snapshot):
        """响应工具调用的流片段"""
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

    @override
    def on_event(self, event):
        """
        响应 'requires_action' 事件
        """
        if event.event == 'thread.run.requires_action':

            run_id = event.data.id  # 获取 run ID
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            arguments = json.loads(tool.function.arguments)
            print(
                f"{tool.function.name}({arguments})",
                flush=True
            )
            # 运行 function
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": available_functions[tool.function.name](
                    **arguments
                )}
            )

        # 提交 function 的结果，并继续运行 run
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        """提交function结果，并继续流"""
        with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
        ) as stream:
            stream.until_done()

from openai import OpenAI

# 初始化 OpenAI 服务


client = OpenAI()


instructions = ("你是MateGen，一个交互式智能编程助手，由九天老师大模型技术团队开发，旨在为数据技术人提供高效稳定的智能辅助编程服务。你具备如下能力："
                "1. 拥有无限对话上下文记忆能力，除非用户主动删除聊天记录，否则你可以永久的记住用户对话信息，这项能力能够让你在和用户交互的过程中逐渐深入理解用户需求，你可以“越用越懂用户”；)"
                "2.强大的本地知识库问答能力，你具备强大的RAG功能，可以在海量文本中进行高精度检索，支持用户围绕自己的本地文本进行进行知识库问答；"
                "3.本地代码解释器功能，你可以连接用户本地的Python环境，并可以随时根据用户的需求，编写高准确率的Python代码，并在用户本地环境运行代码，从而辅助用户完成编程任务。你可以调用python_inter完成Python编程任务，或调用fig_inter函数完成Python绘图任务；"
                "4.NL2SQL功能，你可以连接用户本地的MySQL环境，并根据用户需求编写SQL代码，并在用户MySQL数据库中执行，从而协助用户高效率完成查数、提数等相关工作。你可以调用sql_inter完成查数任务，并使用extract_data函数将MySQL的数据读取到当前Python环境中；"
                "5.你还具备多模态能力，当用户输入图片url地址时，你可以围绕用户输入的图片进行信息识别，并且允许一次性输入多张图片。你可以调用image_recognition函数来完成图像识别工作；"
                "6.你还具备联网功能，当用户的提问超出你的知识库范畴的时候，你可以调用联网功能，先在互联网上搜集相关信息，再进行回答。你看可以调用get_answer函数在知乎上搜索相关信息，也可以调用get_answer_github函数在Github上获取相关信息；"
                "7.除此之外，你可以辅导用户进行Kaggle竞赛，你可以借助Kaggle API搜索竞赛相关信息，并且自动下载热门Kernel并构建知识库，据此辅导用户参与Kaggel竞赛；"
                "8.你还可以辅导用户进行论文解读、数据分析报告编写等，更多功能，欢迎用户在使用过程中探索。总之，你是目前市面上性能强悍、功能稳定的智能编程助手。"
                "目前项目所处阶段："
                "本Agent项目正在内测阶段，只开放了在线服务版本，尚未开放本地部署版本。用户需要联系客服小可爱微信：littlelion_1215，回复“MG”来领取或购买在线服务的API - KEY。"
                "内测阶段结束后，会尽快上线本地部署的开源版本。"
                "请在回复中保持友好、支持和耐心。"
                "这是你能够连接到的MySQL信息：host: 192.168.110.131, port: 3306, user: root, passwd: snowball950123, db: mategen,")


assistant = client.beta.assistants.create(
    instructions=instructions,
    model="gpt-4o",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "python_inter",
                "description": "Executes Python code and returns the result or error message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "py_code": {
                            "type": "string",
                            "description": "The Python code to execute, passed as a string."
                        },
                        "g": {
                            "type": "object",
                            "description": "A dictionary representing the global variables environment. If not provided, a new empty dictionary will be used.",
                            "default": {}
                        }
                    },
                    "required": ["py_code"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "sql_inter",
                "description": "Executes a SQL query on a MySQL database using pymysql and returns the results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sql_query": {
                            "type": "string",
                            "description": "The SQL query to be executed against the MySQL database."
                        },
                        "host": {
                            "type": "string",
                            "description": "The hostname of the MySQL server."
                        },
                        "user": {
                            "type": "string",
                            "description": "The username for the MySQL server."
                        },
                        "password": {
                            "type": "string",
                            "description": "The password for the MySQL server."
                        },
                        "database": {
                            "type": "string",
                            "description": "The name of the database to connect to on the MySQL server."
                        },
                        "port": {
                            "type": "integer",
                            "description": "The port number on which the MySQL server is running."
                        }
                    },
                    "required": ["sql_query", "host", "user", "password", "database", "port"]
                },
            }
        }
    ]
)



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
    finally:
        db_session.close()  # 确保关闭会话

    # 返回 JSON 格式的查询结果

    return json.dumps(results_list)



# 可以被回调的函数放入此字典
available_functions = {
    "python_inter": python_inter,
    "sql_inter":sql_inter
}

# 创建 thread
thread = client.beta.threads.create()

# 添加 user message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="帮我查询 我数据库中 都有哪些 表",
)
# 使用 stream 接口并传入 EventHandler
with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler(),
) as stream:
    stream.until_done()