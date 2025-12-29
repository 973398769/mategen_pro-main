from typing_extensions import override
from openai import AssistantEventHandler
import json

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        """Respond to reply creation event"""
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        """Respond to output generation stream fragments"""
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        """Respond to tool call"""
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_tool_call_delta(self, delta, snapshot):
        """Respond to tool call stream fragments"""
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
        Respond to 'requires_action' event
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
        """Submit function results and continue stream"""
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


instructions = ("You are MateGen, an interactive coding assistant designed to provide reliable, high-quality support for data practitioners. "
                "Capabilities: "
                "1. Persistent conversation memory (until the user clears history), enabling deeper understanding over time. "
                "2. RAG-based local knowledge-base Q&A over large text corpora. "
                "3. Local Python code interpreter: connect to the user's environment, write accurate code, and run locally. Use python_inter or fig_inter for Python and plotting. "
                "4. NL2SQL: connect to local MySQL, write/execute SQL. Use sql_inter and extract_data to load data into Python. "
                "5. Multimodal image understanding via image_recognition. "
                "6. Web search for out-of-knowledge questions (get_answer, get_answer_github). "
                "7. Kaggle assistance using the Kaggle API. "
                "8. Paper reading and data-report drafting. Be friendly, supportive, and patient. "
                "MySQL connection info: host: 192.168.110.131, port: 3306, user: root, passwd: snowball950123, db: mategen,")


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
    Execute Python code and return the final result.
    :param py_code: Python code as a string
    :param g: Dict representing the environment; a new dict is created if not provided
    :return: Result of the code execution
    """
    if g is None:
        g = {}  # 使用空字典作为默认全局环境

    """
    Execute a SQL query against MySQL and return the results.
    Uses pymysql via SQLAlchemy to connect and run queries.
    :param sql_query: SQL query string to run against the MySQL database
    :param host: MySQL server hostname
    :param user: MySQL server username
    :param password: MySQL server password
    :param database: MySQL database name
    :param port: MySQL server port
    :param g: Environment variable (unused); keep default
    :return: Query results as JSON
    """
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
    content="List all tables in my database",
)
# 使用 stream 接口并传入 EventHandler
with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler(),
) as stream:
    stream.until_done()