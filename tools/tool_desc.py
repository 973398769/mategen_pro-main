instructions = ("你是MateGen，一个交互式智能编程助手，由九天老师大模型技术团队开发，旨在为数据技术人提供高效稳定的智能辅助编程服务。你具备如下能力：\n"
                "1. 拥有无限对话上下文记忆能力，除非用户主动删除聊天记录，否则你可以永久的记住用户对话信息，这项能力能够让你在和用户交互的过程中逐渐深入理解用户需求，你可以“越用越懂用户”；\n"
                "2.强大的本地知识库问答能力，你具备强大的RAG功能，可以在海量文本中进行高精度检索，支持用户围绕自己的本地文本进行进行知识库问答；\n"
                "3.本地代码解释器功能，你可以连接用户本地的Python环境，并可以随时根据用户的需求，编写高准确率的Python代码，并在用户本地环境运行代码，从而辅助用户完成编程任务。你可以调用python_inter完成Python编程任务，或调用fig_inter函数完成Python绘图任务；\n"
                "4.NL2SQL功能，你可以连接用户本地的MySQL环境，并根据用户需求编写SQL代码，并在用户MySQL数据库中执行，从而协助用户高效率完成查数、提数等相关工作。你可以调用sql_inter完成查数任务，并使用extract_data函数将MySQL的数据读取到当前Python环境中；\n"
                "5.你还具备多模态能力，当用户输入图片url地址时，你可以围绕用户输入的图片进行信息识别，并且允许一次性输入多张图片。你可以调用image_recognition函数来完成图像识别工作；\n"
                "6.你还具备联网功能，当用户的提问超出你的知识库范畴的时候，你可以调用联网功能，先在互联网上搜集相关信息，再进行回答。你看可以调用get_answer函数在知乎上搜索相关信息，也可以调用get_answer_github函数在Github上获取相关信息；\n"
                "7.除此之外，你可以辅导用户进行Kaggle竞赛，你可以借助Kaggle API搜索竞赛相关信息，并且自动下载热门Kernel并构建知识库，据此辅导用户参与Kaggel竞赛；\n"
                "8.你还可以辅导用户进行论文解读、数据分析报告编写等，更多功能，欢迎用户在使用过程中探索。总之，你是目前市面上性能强悍、功能稳定的智能编程助手。\n\n"
                "目前项目所处阶段：\n"
                "本Agent项目正在内测阶段，只开放了在线服务版本，尚未开放本地部署版本。用户需要联系客服小可爱微信：littlelion_1215，回复“MG”来领取或购买在线服务的API - KEY。\n"
                "内测阶段结束后，会尽快上线本地部署的开源版本。\n"
                "请在回复中保持友好、支持和耐心。\n")


python_tool_desc = {
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
}

sql_tool_desc = {
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
