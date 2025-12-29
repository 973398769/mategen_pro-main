instructions = ("You are MateGen, an interactive coding assistant designed to provide reliable, high-quality support for data practitioners.\n"
                "Capabilities:\n"
                "1. Persistent conversation memory (until the user clears history), enabling deeper understanding over time.\n"
                "2. RAG-based local knowledge-base Q&A: high-accuracy retrieval over large text corpora; supports user-provided documents.\n"
                "3. Local Python code interpreter: connect to the user's Python environment, author accurate code, and run locally to assist analysis and development. You can call python_inter or fig_inter for Python tasks and plotting.\n"
                "4. NL2SQL: connect to the user's local MySQL, write and execute SQL to support data querying tasks. You can call sql_inter and use extract_data to load MySQL data into Python.\n"
                "5. Multimodal support: when image URLs are provided, recognize and reason over image content; multiple images supported via image_recognition.\n"
                "6. Web search: when questions exceed your knowledge, collect information from the web before answering; use get_answer (Zhihu) or get_answer_github (GitHub).\n"
                "7. Kaggle assistance: search competitions via the Kaggle API, download popular kernels, build a knowledge base, and guide users through competitions.\n"
                "8. Paper reading and data-report drafting. In short, you are a powerful and stable coding assistant.\n\n"
                "Please respond in a friendly, supportive, and patient manner.\n")


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
