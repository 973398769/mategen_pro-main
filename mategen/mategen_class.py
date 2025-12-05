from __future__ import annotations
from IPython.display import display, Markdown
from IPython import get_ipython
import time
import os
import json
from openai import OpenAIError
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv, set_key

import uuid
import re
import shutil
import requests


import pandas as pd
import html2text


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
from openai import OpenAI

from typing_extensions import override

import openai
from openai import AsyncOpenAI

from tools.tool_fun import python_inter, sql_inter

from server.cache.base_cache import CachePool
from db.base_model import (SecretModel,
                           KnowledgeBase,
                           ThreadModel,
                           FileInfo)
from server.utils import (SessionLocal,
                          find_env_file,
                          store_thread_info,
                          find_vector_store_id_by_id,
                          get_db_connection_description)

from server.identity_verification.decryption import decrypt_string
from server.agent.create_assistant import generate_assistant
from config.config import assistant_instructions
from tools.tool_desc import python_tool_desc, sql_tool_desc
import logging




logging.basicConfig(level=logging.INFO)
from config.config import setup_logging

# # Call function to set up logging
setup_logging()


class MateGenClass:
    # Class attribute: all instances share the same cache pool
    cache_pool = CachePool()

    @staticmethod
    def get_cache_pool():
        return MateGenClass.cache_pool

    def __init__(self,
                 # user_id,
                 thread_id=None,
                 enhanced_mode=False,
                 knowledge_base_chat=False,
                 knowledge_base_name_id=None,
                 db_name_id=None):

        """
        Initial parameter explanation:
        api_key: Required parameter, represents the string key necessary for calling OpenAI models. No default value, users need to set it in advance to use MateGen. For api-key acquisition and token purchase: Add customer service: littlelion_1215, reply "MG" for details. During MateGen testing period, free gift of 100 billion tokens while supplies last~

        enhanced_mode: Optional parameter, indicates whether to enable enhanced mode. When enhanced mode is enabled, MateGen performance will significantly improve in all aspects, but will also consume token quota more rapidly.

        knowledge_base_name: Optional parameter, represents knowledge base name. When a string name is input, knowledge base Q&A mode will be enabled by default. Note that we need to manually place documents in the knowledge base to proceed smoothly with knowledge base Q&A. Note that if a Kaggle competition name is input here and kaggle_competition_guidance is set to True, Kaggle tutorial mode will be enabled. MateGen will automatically access the Kaggle API for competition information search and popular Kernel search, and automatically build a knowledge base with the same name and enable knowledge base Q&A mode. In this case, files do not need to be placed manually.

        kaggle_competition_guidance: Optional parameter, indicates whether to enable Kaggle tutorial mode. When Kaggle tutorial mode is enabled, a correct Kaggle competition name needs to be input in the knowledge_base_name parameter position. Note that competition tutorial mode can only be enabled when internet connection is smooth.

        """

        # Basic property definition
        self.enhanced_mode = enhanced_mode
        self.knowledge_base_chat = knowledge_base_chat
        self.knowledge_base_name_id = knowledge_base_name_id
        self.db_name_id = db_name_id
        self.vector_id = None
        self.base_path = None
        self.thread_id = thread_id
        self.knowledge_base_description = ''

        # First write static placeholder
        user_id = "fufankongjian"

        # Find api_key based on user id
        db_session = SessionLocal()
        agent_info = db_session.query(SecretModel).filter(SecretModel.user_id == user_id).first()

        # Load environment variables
        dotenv_path = find_env_file()  # Call function
        load_dotenv(dotenv_path)  # Load environment variables
        base_url = os.getenv('BASE_URL')

        # Try to get existing client from cache pool
        client = self.cache_pool.get_client(user_id)

        if client:
            # If exists, use it directly
            self.client = client
            logging.info(f"Reusing client: {self.client}")")
        else:
            # If doesn't exist, create new client and store in cache pool
            if base_url == '':
                self.client = OpenAI(api_key=agent_info.api_key)
            else:
                self.client = OpenAI(api_key=agent_info.api_key,
                                         base_url=base_url)
            logging.info(f"Creating new client: {self.client}")
            self.cache_pool.set_client(user_id, self.client)
            logging.info(f"Completed client caching: {self.client}")

        async_client = self.cache_pool.get_async_client(user_id)
        if async_client:
            logging.info(f"Reusing async_client: {async_client}")
        else:
            if base_url == '':
                async_client = AsyncOpenAI(api_key=agent_info.api_key)
            else:
                async_client = AsyncOpenAI(api_key=agent_info.api_key,
                                           base_url=base_url)
            logging.info(f"Creating new async_client: {async_client}")
            self.cache_pool.set_async_client(user_id, async_client)
            logging.info(f"Completed async_client caching: {async_client}")

        logging.info("Initializing MateGen object instance, please wait...")ct instance, please wait...")

        # Check OpenAI instance connectivity:
        try:
            # Step 1. Instantiate Assistant object
            if self.client.models.list(timeout=5):
                logging.info("API_KEY verified, successfully connected to server...")ully connected to server...")
                # First check thread pool for assistant object
                assistant = self.cache_pool.get_assistant(user_id)
                if assistant:
                    self.assis_id = assistant
                    logging.info(f"Reusing assistant instance: {self.assis_id}")lf.assis_id}")
                else:
                    if not agent_info.initialized:
                        logging.info("First time using MateGen, initializing Agent settings...")
                        # Generate assistant idant id
                        self.assis_id = generate_assistant(self.client, enhanced_mode)

                        # Update database info
                        agent_info.initialized = True
                        agent_info.assis_id = self.assis_id
                        db_session.commit()
                        logging.info(f"Created new assistant instance: {self.assis_id}")
                        # Add assistant to thread pool
                        self.cache_pool.set_assistant(user_id, self.assis_id)
                        logging.info(f"Completed assistant caching: {self.assis_id}")
                    else:
                        self.assis_id = agent_info.assis_id
                        logging.info(f"Reusing assistant instance: {self.assis_id}")
                        self.cache_pool.set_assistant(user_id, self.assis_id)
                        logging.info(f"Completed assistant caching: {self.assis_id}")
                # Instantiate Thread object, instantiate during conversation execution
                if self.thread_id is None:  # New conversation logic
                    agent = db_session.query(SecretModel).filter(SecretModel.user_id == user_id).first()
                    thread = db_session.query(ThreadModel).filter(
                        ThreadModel.agent_id == agent.assis_id,
                        ThreadModel.conversation_name == 'new_chat'
                    ).first()
                    if thread:
                        self.thread_id = thread.id
                        logging.info(f"Reusing thread instance: {self.thread_id}")
                    else:
                        # Determine run mode based on whether knowledge base conversation feature is enabled
                        run_mode = "kb" if self.knowledge_base_chat else "normal"
                        thread = self.client.beta.threads.create()
                        store_thread_info(db_session, self.assis_id, thread.id, 'new_chat', run_mode)
                        self.thread_id = thread.id
                        logging.info(f"Created new thread instance: {self.thread_id}")

                    self.cache_pool.add_thread(self.assis_id, self.thread_id)
                    logging.info(f"Completed thread caching: {self.thread_id}")
                else:
                    self.thread_id = thread_id
                    logging.info(f"Reusing thread instance: {self.thread_id}")

                # If knowledge base or database is selectedbase or database is selected
                if self.knowledge_base_name_id or self.db_name_id:
                    tools = []
                    instructions = assistant_instructions  # Initialize base instructions
                    # Process KnowledgeBase
                    if self.knowledge_base_name_id:
                        real_kb_name = db_session.query(KnowledgeBase).filter(
                            KnowledgeBase.id == self.knowledge_base_name_id).one_or_none()
                        if real_kb_name:
                            self.knowledge_base_name = real_kb_name.knowledge_base_name
                            self.vector_id = find_vector_store_id_by_id(db_session, self.knowledge_base_name_id)
                    # Process Database Description
                    db_description = ""
                    if self.db_name_id is not None:
                        db_description = get_db_connection_description(db_session, self.db_name_id)
                        tools.append(python_tool_desc)
                        tools.append(sql_tool_desc)
                    # Update instruction string
                    if db_description:
                        instructions += "\n" + "    " + db_description
                    # Update Assistant settings
                    tool_resources = {}
                    if self.knowledge_base_name_id:
                        tools.append({"type": "file_search"})
                        tool_resources = {"file_search": {"vector_store_ids": [self.vector_id]}}

                    self.client.beta.assistants.update(
                        self.assis_id,
                        instructions=instructions,
                        tools=tools,
                        tool_resources=tool_resources,
                    )
                    logging.info(f"Updated assistant object instance")

                db_session.close()
            else:
                logging.info("Current network environment cannot connect to server, please check network and try again later...")

            logging.info("Initialization complete, MateGen ready to use!")

        except openai.AuthenticationError:
            logging.info(
                "API-KEY not verified.")
        except openai.APIConnectionError:
            logging.info("Current network environment cannot connect to server, please check network and try again later...")
        except openai.RateLimitError:
            logging.info(
                "API-KEY account has reached RateLimit upper limit.")
        except openai.OpenAIError as e:
            logging.info(f"An error occurred: {e}")

    async def create_thread(self, client):
        return client.beta.threads.create()

    def initialize(self) -> tuple:
        return self.assis_id, self.thread_id

    def chat(self, question=None, chat_stream=False) -> tuple:
        if question != None:
            db_session = SessionLocal()

            local_conversation_name = db_session.query(ThreadModel).filter(
                ThreadModel.id == self.thread_id).one_or_none()

            if local_conversation_name.conversation_name == "new_chat":
                local_conversation_name.conversation_name = question[:20] if len(question) > 20 else question
                db_session.commit()

            db_session.close()
            return self.assis_id

    def upload_knowledge_base(self, knowledge_base_name=None):
        if knowledge_base_name != None:
            self.knowledge_base_name = knowledge_base_name
        elif self.knowledge_base_name == None:
            self.knowledge_base_name = input("Please enter the knowledge base name to update: ")

        if not is_folder_not_empty(self.knowledge_base_name):
            print(f"Knowledge base folder: {self.knowledge_base_name} is empty, please place files before updating the knowledge base.")
            return None
        else:
            self.vector_id = create_knowledge_base(self.client, self.knowledge_base_name)
            if self.vector_id != None:
                print(f"Successfully updated knowledge base {self.knowledge_base_name}")

    def update_knowledge_base(self):
        knowledge_base_name, vector_id = print_and_select_knowledge_base_to_update()
        if knowledge_base_name != None:
            self.upload_knowledge_base(knowledge_base_name=knowledge_base_name)

    def get_knowledge_base_vsid(self, knowledge_base_name=None):
        if knowledge_base_name != None:
            self.knowledge_base_name = knowledge_base_name
        elif self.knowledge_base_name == None:
            self.knowledge_base_name = input("Please enter the knowledge base name to get ID: ")

        knowledge_base_name = self.knowledge_base_name + '!!' + self.client.api_key[8:]
        check_res = check_knowledge_base_name(client=self.client,
                                              knowledge_base_name=knowledge_base_name)

        if check_res == None:
            print("Knowledge base has not been created or has expired, please recreate the knowledge base.")
            return None
        else:
            return check_res

    def set_knowledge_base_url(self, base_url):
        if self.is_valid_directory(base_url):
            set_key(dotenv_path, 'KNOWLEDGE_LIBRARY_PATH', base_url)
            return True
        else:
            return False

    def set_base_url(self, base_url):
        if self.is_valid_base_url(base_url):
            set_key(dotenv_path, 'BASE_URL', base_url)
            print(f"Updated base_url address: {base_url}")
        else:
            print(f"Invalid base_url address: {base_url}")

    def is_valid_base_url(self, path):
        original_string = decrypt_string(self.api_key, key=b'YAboQcXx376HSUKqzkTz8LK1GKs19Skg4JoZH4QUCJc=')
        split_strings = original_string.split(' ')
        s1 = split_strings[0]
        client_tmp = OpenAI(api_key=s1,
                            base_url=path)

        models_tmp = client_tmp.models.list()
        print(f"models_tmp = {models_tmp}")
        return models_tmp

    def is_valid_directory(self, path):
        """
        Check if the path is a valid directory path
        """
        # Check if the path is an absolute path
        if not os.path.isabs(path):
            return False

        # Check if the path exists and is a directory
        if not os.path.isdir(path):
            return False

        return True

    def write_knowledge_base_description(self, description):
        """
        Update knowledge base description
        """
        self.knowledge_base_description = description
        update_knowledge_base_description(self.knowledge_base_name,
                                          self.knowledge_base_description)

    def debug(self):
        res = input(
            'Note: The debug function can only capture the error result from the previous cell run, and it only works smoothly when the MateGen module naming variables match the current code environment. In other cases, please manually copy the code and error information, and input it to MateGen through the chat method for more accurate debugging. Continue using debug function: 1. Continue; 2. Exit')
        if res == '1':
            current_globals = globals()

            ipython = get_ipython()
            history = list(ipython.history_manager.get_range())

            if not history:
                print("No historical code records, unable to start automatic debug function.")
            else:
                last_session, last_line_number, last_cell_code = history[-2]
                try:
                    exec(last_cell_code, current_globals)
                except Exception as e:
                    error_info = str(e)
                    user_input = f"Hello, my code encountered an error. Please help me check the code and explain the error cause. Code: {last_cell_code}, Error message: {error_info}"
                    chat_base_auto_cancel(user_input=user_input,
                                          assistant_id=self.s3,
                                          client=self.client,
                                          thread_id=self.thread_id,
                                          run_id=None,
                                          first_input=True,
                                          tool_outputs=None)
        else:
            print("Please call MateGen's chat function and manually copy the error code and error message for precise debugging.")

    def clear_messages(self):
        client.beta.threads.delete(thread_id=self.thread_id)
        thread = client.beta.threads.create()
        self.thread = thread
        self.thread_id = thread.id
        log_thread_id(self.thread_id)
        print("Historical messages have been cleared")

    def reset(self):
        try:
            home_dir = str(Path.home())
            log_dir = os.path.join(home_dir, "._logs")
            shutil.rmtree(log_dir)
            print("已重置成功！请重新创建MateGen并继续使用。")

        except Exception as e:
            print("重置失败，请重启代码环境，并确认API-KEY后再尝试重置。")

    def reset_account_info(self):
        res = input("账户重置功能将重置全部知识库在线存储文档、词向量数据库和已创建的Agent，是否继续：1.继续；2.退出。")
        if res == '1':
            print("正在重置账户各项信息...")
            print("正在删除在线知识库中全部文档文档...")
            delete_all_files(self.client)
            print("正在删除知识库的词向量存储...")
            delete_all_vector_stores(self.client)
            print("正在删除已创建的Agent")
            delete_all_assistants(self.client)
            print("正在重置Agent信息")
            self.reset()
            print("已重置成功重置账户！请重新创建MateGen并继续使用。")
        else:
            return None

    def print_usage(self):
        print_token_usage()
        print("Local token count may be inaccurate, actual token consumption is based on server data.")


# Functions that can be called are placed in this dictionary
available_functions = {
    "python_inter": python_inter,
    "sql_inter": sql_inter
}

from openai.lib.streaming import AsyncAssistantEventHandler


# print(f"dotenv_path: {dotenv_path}")
class EventHandler(AsyncAssistantEventHandler):

    @override
    async def on_text_created(self, text) -> None:
        """响应回复创建事件"""

    @override
    async def on_text_delta(self, delta, snapshot) -> None:
        """响应输出生成的流片段"""
        # print(delta.value, end='', flush=True)
        pass

    from openai.types.beta.threads.message import Message
    async def on_message_done(self, message: Message) -> None:
        """Callback that is fired when a message is completed"""
        # We keep this empty as in the original version,
        # but with logging replaced by print, it would be:
        # print(f"Message done: {message}")

    @override
    async def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id
            await self.handle_requires_action(event.data, run_id)

    async def handle_requires_action(self, data, run_id):

        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            arguments = json.loads(tool.function.arguments)
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": available_functions[tool.function.name](**arguments)
            })

        await self.submit_tool_outputs(tool_outputs, run_id)

    async def submit_tool_outputs(self, tool_outputs, run_id):
        mategen_instance = MateGenClass()
        client = mategen_instance.cache_pool.get_async_client(user_id="fufankongjian")
        async with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
        ) as stream:
            await stream.until_done()


def create_knowledge_base_folder(sub_folder_name=None):
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')

    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    # 创建 base_path 文件夹
    os.makedirs(base_path, exist_ok=True)

    # 检查并创建主目录 JSON 文件
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        with open(main_json_file, 'w') as f:
            json.dump({}, f, indent=4)

    # 如果 sub_folder_name 不为空，则在 base_path 内创建子文件夹
    if sub_folder_name:
        sub_folder_path = os.path.join(base_path, sub_folder_name)
        os.makedirs(sub_folder_path, exist_ok=True)

        # 检查并创建子目录 JSON 文件
        sub_json_file = os.path.join(sub_folder_path, f'{sub_folder_name}_vector_id.json')
        if not os.path.exists(sub_json_file):
            with open(sub_json_file, 'w') as f:
                json.dump({"vector_db_id": None, "knowledge_base_description": ""}, f, indent=4)

        return sub_folder_path
    else:
        return base_path


def create_knowledge_base(client,
                          kb_id,
                          knowledge_base_name,
                          chunking_strategy="auto",
                          max_chunk_size_tokens=800,
                          chunk_overlap_tokens=400,
                          thread_id=None):
    logging.info("正在创建知识库的向量存储，请稍后...")
    db_session = SessionLocal()
    # 这里用来存储展示的知识库名称
    display_knowledge_base_name = knowledge_base_name
    knowledge_base_info = db_session.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).one_or_none()
    knowledge_base_name = knowledge_base_info.knowledge_base_name

    file_ids = db_session.query(FileInfo.id).filter(FileInfo.knowledge_base_id == kb_id).all()
    file_ids = [file_id[0] for file_id in file_ids]

    print(f"kb_id:{kb_id}")
    if chunking_strategy == "auto":
        vector_store = client.beta.vector_stores.create(name=knowledge_base_name)
        client.beta.vector_stores.file_batches.create(vector_store_id=vector_store.id, file_ids=file_ids)
    else:
        vector_store = client.beta.vector_stores.create(
            name=knowledge_base_name,  # 你提供的向量存储名称
            chunking_strategy={
                "type": "static",  # 明确使用 static 切分策略
                "static": {  # 在 static 键下提供具体的切分参数
                    "max_chunk_size_tokens": max_chunk_size_tokens,  # 自定义的最大切分大小
                    "chunk_overlap_tokens": chunk_overlap_tokens  # 自定义的重叠大小
                }
            }
        )
        client.beta.vector_stores.file_batches.create(vector_store_id=vector_store.id, file_ids=file_ids)

    vector_id = vector_store.id

    try:
        knowledge_base = db_session.query(KnowledgeBase).filter(
            KnowledgeBase.id == kb_id
        ).one_or_none()

        if knowledge_base is None:
            # 如果没有找到知识库，可以选择抛出异常或返回一个错误消息
            return None

        # 更新各个字段并打印状态

        knowledge_base.vector_store_id = vector_id
        knowledge_base.display_knowledge_base_name = display_knowledge_base_name
        knowledge_base.thread_id = thread_id
        knowledge_base.chunking_strategy = chunking_strategy
        knowledge_base.max_chunk_size_tokens = max_chunk_size_tokens
        knowledge_base.chunk_overlap_tokens = chunk_overlap_tokens

        db_session.commit()  # 提交更改

        logging.info("知识库创建完成！")
        return vector_id

    except Exception as e:
        logging.info(e)


def ensure_file_exists(file_path, timeout=10):
    """
    确保文件存在
    :param file_path: 文件路径
    :param timeout: 等待时间（秒）
    :return: 文件是否存在
    """
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            print(f"超时 {timeout} 秒，文件 {file_path} 仍不存在。")
            return False
        time.sleep(1)
    return True


def convert_keyword(q):
    """
    将用户输入的问题转化为适合在知乎上进行搜索的关键词
    """
    global client

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "你专门负责将用户的问题转化为知乎网站搜索关键词，只返回一个你认为最合适的搜索关键词即可"},
            {"role": "user", "content": "请帮我介绍下Llama3模型基本情况"},
            {"role": "assistant", "content": "Llama3模型介绍"},
            {"role": "user", "content": q}
        ]
    )
    q = completion.choices[0].message.content
    return q


def convert_keyword_github(q):
    """
    将用户输入的问题转化为适合在Github上进行搜索的关键词
    """
    global client

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "你专门负责将用户的问题转化为Github上的搜索关键词，只返回一个你认为最合适的搜索关键词即可"},
            {"role": "user", "content": "请问DeepSpeed是什么？"},
            {"role": "assistant", "content": "DeepSpeed"},
            {"role": "user", "content": q}
        ],
    )
    q = completion.choices[0].message.content
    return q


def image_recognition(url_list, question, g='globals()'):
    global client
    """
    根据图片地址，对用户输入的图像进行识别，最终返回用户提问的答案
    :param url_list: 用户输入的图片地址（url）列表，每个图片地址都以字符串形式表示
    :param question: 用户提出的对图片识别的要求
    :param g: g，字符串形式变量，表示环境变量，无需设置，保持默认参数即可
    :return：图片识别的结果
    """

    model = os.getenv('VISION_MODEL')

    content = []
    content.append({'type': 'text', 'text': question})
    for url in url_list:
        content.append(
            {'type': 'image_url',
             'image_url': {'url': url}
             }
        )
    messages = [
        {'role': 'user',
         'content': content
         }
    ]

    print("正在对图像内容进行识别...")
    response = client.chat.completions.create(
        model=model,
        messages=messages)

    return response.choices[0].message.content


def log_thread_id(thread_id):
    global thread_log_file
    try:
        with open(thread_log_file, "r") as file:
            thread_log = json.load(file)
    except FileNotFoundError:
        thread_log = []

    # 添加新的线程 ID
    thread_log.append(thread_id)

    with open(thread_log_file, "w") as file:
        json.dump(thread_log, file)


def get_latest_thread(client):
    global thread_log_file
    try:
        with open(thread_log_file, "r") as file:
            thread_log = json.load(file)
    except FileNotFoundError:
        thread_log = []

    if thread_log:
        # 获取最新的线程 ID 并将其设置为全局变量
        thread_id = thread_log[-1]
        thread = client.beta.threads.retrieve(thread_id=thread_id)
        return thread
    else:
        # 如果没有线程，则创建一个新的线程
        thread = client.beta.threads.create()
        log_thread_id(thread.id)
        return thread


def log_token_usage(thread_id, tokens):
    global token_log_file
    try:
        with open(token_log_file, "r") as file:
            token_log = json.load(file)
    except FileNotFoundError:
        token_log = {"total_tokens": 0}

    today = datetime.utcnow().date().isoformat()

    if today not in token_log:
        token_log[today] = {}

    if thread_id not in token_log[today]:
        token_log[today][thread_id] = 0
    token_log[today][thread_id] += tokens

    # 更新累计 token 总数
    if "total_tokens" not in token_log:
        token_log["total_tokens"] = 0
    token_log["total_tokens"] += tokens

    with open(token_log_file, "w") as file:
        json.dump(token_log, file)


def print_token_usage():
    global token_log_file
    try:
        with open(token_log_file, "r") as file:
            token_log = json.load(file)
    except FileNotFoundError:
        print("目前没有token消耗")
        return

    today = datetime.utcnow().date().isoformat()

    # 打印今日 token 使用情况
    if today in token_log:
        total_tokens_today = sum(token_log[today].values())
        print(f"今日已消耗的 token 数量：{total_tokens_today}")
    else:
        print("今日没有消耗 token。")

    # 打印累计 token 使用情况
    total_tokens = token_log.get("total_tokens", 0)
    print(f"总共消耗的 token 数量：{total_tokens}")


def get_agent_info():
    global agent_info_file
    try:
        with open(agent_info_file, "r") as file:
            agent_info = json.load(file)
    except FileNotFoundError:
        print("Agent信息日志文件不存在。")
        return None

    return agent_info


def make_hl():
    global home_dir, log_dir, thread_log_file, token_log_file, agent_info_file
    home_dir = str(Path.home())
    log_dir = os.path.join(home_dir, "._logs")
    os.makedirs(log_dir, exist_ok=True)
    token_log_file = os.path.join(log_dir, "token_usage_log.json")
    thread_log_file = os.path.join(log_dir, "thread_log.json")
    agent_info_file = os.path.join(log_dir, "agent_info_log.json")

    if not os.path.exists(thread_log_file):
        with open(thread_log_file, "w") as f:
            json.dump([], f)  # 创建一个空列表

    if not os.path.exists(token_log_file):
        with open(token_log_file, "w") as f:
            json.dump({"total_tokens": 0}, f)


def download_files_and_create_kb(client, file_info_json):
    home_dir = str(Path.home())
    kb_name = get_agent_info()['agent_type']
    storage_path = os.path.join(home_dir, f"._logs/{kb_name}")
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    file_info = json.loads(file_info_json)

    print("正在同步Agent基础文件，这会需要一些时间，请耐心等待...")
    for file_name, file_url in file_info.items():
        try:
            response = requests.get(file_url)
            response.raise_for_status()

            file_path = os.path.join(storage_path, file_name)

            with open(file_path, 'wb') as file:
                file.write(response.content)
        except requests.exceptions.RequestException as e:
            print(f"文件 '{file_name}' 下载失败: {e}")

    vector_id = create_knowledge_base(client=client,
                                      knowledge_base_name=kb_name,
                                      folder_path_base=storage_path)

    return vector_id




def clean_and_convert_to_json(raw_str):
    """
    清理并将不规则的字符串转换为满足JSON格式要求的字符串
    :param raw_str: 不规则的原始字符串
    :return: JSON格式的字符串或错误信息
    """
    # 替换未转义的换行符
    cleaned_str = re.sub(r'\\n', r'\\\\n', raw_str)
    # 替换未转义的单引号
    cleaned_str = re.sub(r'(?<!\\)\'', r'\"', cleaned_str)
    # 替换未转义的反斜杠
    cleaned_str = re.sub(r'\\(?=\W)', r'\\\\', cleaned_str)

    # 尝试将清理后的字符串转换为JSON对象
    json_obj = json.loads(cleaned_str)
    # 将JSON对象格式化为字符串
    json_str = json.dumps(json_obj, indent=2, ensure_ascii=False)
    return json_str


def clear_folder(path):
    """
    清理指定路径下的所有文件和子文件夹。

    :param path: 要清理的文件夹路径。
    """
    if os.path.exists(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        # print(f"The path {path} does not exist.")
        pass


def handle_function_args(function_args):
    """
    处理函数参数，检查并转换为JSON格式
    """

    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True

    if not is_json(function_args):
        try:
            function_args = clean_and_convert_to_json(function_args)
        except Exception as e:
            pass

    if not is_json(function_args):
        return None

    return json.loads(function_args)


def print_code_if_exists(function_args):
    """
    如果存在代码片段，则打印代码
    """

    def convert_to_markdown(code, language):
        return f"```{language}\n{code}\n```"

    # 如果是SQL，则按照Markdown中SQL格式打印代码
    if function_args.get('sql_query'):
        code = function_args['sql_query']
        markdown_code = convert_to_markdown(code, 'sql')
        print("即将执行以下代码：")
        display(Markdown(markdown_code))

    # 如果是Python，则按照Markdown中Python格式打印代码
    elif function_args.get('py_code'):
        code = function_args['py_code']
        markdown_code = convert_to_markdown(code, 'python')
        print("即将执行以下代码：")
        display(Markdown(markdown_code))


def run_status(assistant_id, client, thread_id, run_id):
    # 创建计数器
    i = 0
    try:
        # 轮询检查运行状态
        while True:
            run_details = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            status = run_details.status

            if status in ['completed', 'expired', 'cancelled']:
                log_token_usage(thread_id, run_details.usage.total_tokens)
                return run_details
            if status in ['requires_action']:
                return run_details
            if status in ['failed']:
                print("当前服务器拥挤，请1分钟后再试。")
                return None

            i += 1
            if i == 30:
                print("响应超时，请稍后再试。")
                return None

            # 等待一秒后再检查状态
            time.sleep(1)

    except OpenAIError as e:
        print(f"An error occurred: {e}")
        return None

    return None


def chat_base(user_input,
              assistant_id,
              client,
              thread_id,
              chat_stream,
              run_id=None,
              first_input=True,
              tool_outputs=None,
              ):
    # 创建消息
    if first_input:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input,
        )

    if tool_outputs == None:
        # 执行对话
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

    else:
        # Function calling第二轮对话，更新run的状态
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs,
        )

    # 判断运行状态
    run_details = run_status(assistant_id=assistant_id,
                             client=client,
                             thread_id=thread_id,
                             run_id=run.id)

    # 若无结果，则打印报错信息
    if run_details == None:
        return {"data": "当前应用无法运行，请稍后再试"}

    # 若消息创建完成，则返回模型返回信息
    elif run_details.status == 'completed':
        messages_check = client.beta.threads.messages.list(thread_id=thread_id)
        chat_res = messages_check.data[0].content[0].text.value
        return {"data": chat_res}

    # 若外部函数响应超时，则根据用户反馈制定执行流程
    elif run_details.status == 'expired' or run_details.status == 'cancelled':
        user_res = input('当前编程环境响应超时或此前任务已取消，是否继续？1.继续，2.重新输入需求')
        if user_res == '1':
            print('好的，正在重新创建响应')
            chat_base_auto_cancel(user_input=user_input,
                                  assistant_id=assistant_id,
                                  client=client,
                                  thread_id=thread_id,
                                  run_id=run_id,
                                  chat_stream=None,
                                  first_input=True,
                                  tool_outputs=None,
                                  )

        else:
            user_res1 = input('请输入新的问题：')
            chat_base_auto_cancel(user_input=user_res1,
                                  assistant_id=assistant_id,
                                  client=client,
                                  thread_id=thread_id,
                                  run_id=run_id,
                                  chat_stream=None,
                                  first_input=True,
                                  tool_outputs=None,
                                  )

    # 若调用外部函数，则开启Function calling
    elif run_details.status == 'requires_action':
        # 创建外部函数输出结果
        tool_outputs = function_to_call(run_details=run_details,
                                        client=client,
                                        thread_id=thread_id,
                                        run_id=run.id)

        chat_base_auto_cancel(user_input=user_input,
                              assistant_id=assistant_id,
                              client=client,
                              thread_id=thread_id,
                              run_id=run.id,
                              chat_stream=None,
                              first_input=False,
                              tool_outputs=tool_outputs)


def extract_run_id(text):
    pattern = r'run_\w+'  # 正则表达式模式，用于匹配以 run_ 开头的字符
    match = re.search(pattern, text)
    if match:
        return match.group(0)  # 返回匹配的字符串
    else:
        return None


def chat_base_auto_cancel(user_input,
                          assistant_id,
                          client,
                          thread_id,
                          chat_stream,
                          run_id=None,
                          first_input=True,
                          tool_outputs=None,
                          ):
    max_attempt = 3
    now_attempt = 0

    while now_attempt < max_attempt:
        try:
            res = chat_base(user_input=user_input,
                            assistant_id=assistant_id,
                            client=client,
                            thread_id=thread_id,
                            run_id=run_id,
                            first_input=first_input,
                            tool_outputs=tool_outputs,
                            chat_stream=chat_stream
                            )

            if res:
                return res
            break  # 成功运行后退出循环

        except OpenAIError as e:
            run_id_to_cancel = extract_run_id(e.body['message'])
            if run_id_to_cancel:
                client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id_to_cancel)
                print(f"已取消运行 {run_id_to_cancel}")
            else:
                print("未找到运行ID，无法取消")

        except Exception as e:
            print(f"程序运行错误: {e}")

        now_attempt += 1

    if now_attempt == max_attempt:
        print("超过最大尝试次数，操作失败")


def move_folder(src_folder, dest_folder):
    """
    将文件夹从 src_folder 剪切到 dest_folder，当目标文件夹存在时覆盖原始文件夹
    """
    try:
        # 确保源文件夹存在
        if not os.path.exists(src_folder):
            print(f"源文件夹不存在: {src_folder}")
            return False

        # 如果目标文件夹存在，删除目标文件夹
        if os.path.exists(dest_folder):
            shutil.rmtree(dest_folder)

        # 确保目标文件夹的父目录存在，如果不存在则创建
        parent_dir = os.path.dirname(dest_folder)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        # 移动文件夹
        shutil.move(src_folder, dest_folder)
        print(f"本地知识库文件夹已从 {src_folder} 移动到 {dest_folder}")
        return True
    except Exception as e:
        print(f"移动文件夹失败: {e}。或由于目标文件夹正在被读取导致，请重启Jupyter并再次尝试。")
        return False


def get_knowledge_base_description(sub_folder_name):
    """
    获取指定知识库的知识库描述内容
    """
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')

    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    # 子文件夹路径
    sub_folder_path = os.path.join(base_path, sub_folder_name)
    sub_json_file = os.path.join(sub_folder_path, f'{sub_folder_name}_vector_id.json')
    # print(sub_json_file)

    # 检查子目录 JSON 文件是否存在
    # if ensure_file_exists(sub_json_file):
    with open(sub_json_file, 'r') as f:
        data = json.load(f)
        description = data.get('knowledge_base_description', "")
        if description:
            return description
        else:
            return False
    # else:
    # print(f"子目录 JSON 文件不存在：{sub_json_file}")
    # return False


def update_knowledge_base_description(sub_folder_name, description):
    """
    更新子目录的 knowledge_base_description 字段
    """
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')

    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    # 子文件夹路径
    sub_folder_path = os.path.join(base_path, sub_folder_name)
    sub_json_file = os.path.join(sub_folder_path, f'{sub_folder_name}_vector_id.json')

    # 检查子目录 JSON 文件是否存在
    # if ensure_file_exists(sub_json_file):
    with open(sub_json_file, 'r+') as f:
        data = json.load(f)
        # 先删除原有的 description 内容
        data['knowledge_base_description'] = ""
        # 再写入新的 description 内容
        data['knowledge_base_description'] = description
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    logging.info(f"已更新知识库：{sub_folder_name}的相关描述")
    return True
    # else:
    # print(f"子目录 JSON 文件不存在：{sub_json_file}")


def print_and_select_knowledge_base():
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')

    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    # 检查主目录 JSON 文件
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        logging.info(f"{main_json_file} 不存在。请先创建知识库。")
        return []

    # 读取主目录 JSON 文件
    with open(main_json_file, 'r') as f:
        main_mapping = json.load(f)

    knowledge_bases = [{"name": key, "vector_db_id": value} for key, value in main_mapping.items()]
    return knowledge_bases

    # while True:
    #     # 打印所有知识库名称
    #     print("知识库列表：")
    #     knowledge_bases = list(main_mapping.keys())
    #     for idx, name in enumerate(knowledge_bases, 1):
    #         print(f"{idx}. {name}")
    #
    #     # 用户选择知识库
    #     try:
    #         selection = int(input("请选择一个知识库的序号（或输入0创建新知识库）：")) - 1
    #         if selection == -1:
    #             new_knowledge_base = input("请输入新知识库的名称：")
    #             # 返回新知识库名称和 None 作为 ID
    #             return new_knowledge_base, None
    #         elif 0 <= selection < len(knowledge_bases):
    #             selected_knowledge_base = knowledge_bases[selection]
    #             vector_db_id = main_mapping[selected_knowledge_base]
    #             return selected_knowledge_base, vector_db_id
    #         else:
    #             print("无效的选择。请再试一次。")
    #     except ValueError:
    #         print("请输入一个有效的序号。")


def print_and_select_knowledge_base_to_update():
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')
    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        print(f"{main_json_file} 不存在。请先创建知识库。")
        return None, None

    # 读取主目录 JSON 文件
    with open(main_json_file, 'r') as f:
        main_mapping = json.load(f)

    while True:
        # 打印所有知识库名称
        print("知识库列表：")
        knowledge_bases = list(main_mapping.keys())
        for idx, name in enumerate(knowledge_bases, 1):
            print(f"{idx}. {name}")

        # 用户选择知识库
        try:
            selection = int(input("请选择一个知识库的序号（或输入0退出）：")) - 1
            if selection == -1:
                return None, None
            elif 0 <= selection < len(knowledge_bases):
                selected_knowledge_base = knowledge_bases[selection]
                vector_db_id = main_mapping[selected_knowledge_base]
                return selected_knowledge_base, vector_db_id
            else:
                print("无效的选择。请再试一次。")
        except ValueError:
            print("请输入一个有效的序号。")


def get_id(keyword):
    load_dotenv()
    headers_json = os.getenv('HEADERS')
    cookies_json = os.getenv('COOKIES')

    headers = json.loads(headers_json)
    cookies = json.loads(cookies_json)

    url = "https://www.kaggle.com/api/i/search.SearchWebService/FullSearchWeb"
    data = {
        "query": keyword,
        "page": 1,
        "resultsPerPage": 20,
        "showPrivate": True
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data).json()

    # 确保搜索结果不为空
    if "documents" not in response or len(response["documents"]) == 0:
        print(f"竞赛： '{keyword}' 并不存在，请登录Kaggle官网并检查赛题是否正确：https://www.kaggle.com/")
        return None

    document = response["documents"][0]
    document_type = document["documentType"]

    if document_type == "COMPETITION":
        item_id = document["databaseId"]
    elif document_type == "KERNEL":
        item_id = document['kernelInfo']['dataSources'][0]['reference']['sourceId']
    else:
        print(f"竞赛： '{keyword}' 并不存在，请登录Kaggle官网并检查赛题是否正确：https://www.kaggle.com/")
        return None

    return item_id


def create_kaggle_project_directory(competition_name):
    # 创建kaggle知识库目录
    kaggle_dir = create_knowledge_base_folder(sub_folder_name=competition_name)

    # 如果 .kaggle 目录不存在，则创建
    # if not os.path.exists(kaggle_dir):
    # os.makedirs(kaggle_dir)
    # print(f"Created directory: {kaggle_dir}")

    # 定义项目目录结构
    # base_dir = os.path.join(kaggle_dir, f"{competition_name}_project")
    # directories = [
    # os.path.join(base_dir, 'knowledge_library'),
    # os.path.join(base_dir, 'data'),
    # os.path.join(base_dir, 'submission'),
    # os.path.join(base_dir, 'module')
    # ]
    # task_schedule_file = os.path.join(base_dir, 'task_schedule.json')

    # 创建目录和文件
    # for directory in directories:
    # if not os.path.exists(directory):
    # os.makedirs(directory)

    # if not os.path.exists(task_schedule_file):
    # with open(task_schedule_file, 'w') as f:
    # json.dump({}, f)

    # print("已完成项目创建")
    return kaggle_dir


def getOverviewAndDescription(_id):
    load_dotenv()
    headers_json = os.getenv('HEADERS')
    cookies_json = os.getenv('COOKIES')

    headers = json.loads(headers_json)
    cookies = json.loads(cookies_json)
    url = "https://www.kaggle.com/api/i/competitions.PageService/ListPages"
    data = {
        "competitionId": _id
    }
    data = json.dumps(data, separators=(',', ':'))
    data = requests.post(url, headers=headers, cookies=cookies, data=data).json()
    overview = {}
    data_description = {}
    for page in data['pages']:
        # print(page['name'])
        overview[page['name']] = page['content']
    if 'rules' in overview: del overview['rules']
    if 'data-description' in overview:
        data_description['data-description'] = overview['data-description']
        del overview['data-description']

    return overview, data_description


def json_to_markdown(json_obj, level=1):
    markdown_str = ""

    for key, value in json_obj.items():
        if isinstance(value, dict):
            markdown_str += f"{'#' * level} {key}\n\n"
            markdown_str += json_to_markdown(value, level + 1)
        else:
            markdown_str += f"{'#' * level} {key}\n\n{value}\n\n"

    return markdown_str


def convert_html_to_markdown(html_content):
    """
    将 HTML 内容转换为 Markdown 格式

    :param html_content: 包含 HTML 标签的文本内容
    :return: 转换后的 Markdown 文本
    """
    h = html2text.HTML2Text()
    h.ignore_links = False  # 设置为 False 以保留链接
    markdown_content = h.handle(html_content)
    return markdown_content


def save_markdown(content, competition_name, file_type):
    # home_dir = str(Path.home())
    # directory = os.path.join(os.path.expanduser(home_dir), f'.kaggle./{competition_name}_project/knowledge_library')
    directory = create_kaggle_project_directory(competition_name)
    filename = f'{competition_name}_{file_type}.md'

    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def get_code(_id):
    load_dotenv()
    headers_json = os.getenv('HEADERS')
    cookies_json = os.getenv('COOKIES')

    headers = json.loads(headers_json)
    cookies = json.loads(cookies_json)
    data = {
        "kernelFilterCriteria": {
            "search": "",
            "listRequest": {
                "competitionId": _id,
                "sortBy": "VOTE_COUNT",
                "pageSize": 20,
                "group": "EVERYONE",
                "page": 1,
                "modelIds": [],
                "modelInstanceIds": [],
                "excludeKernelIds": [],
                "tagIds": "",
                "excludeResultsFilesOutputs": False,
                "wantOutputFiles": False,
                "excludeNonAccessedDatasources": True
            }
        },
        "detailFilterCriteria": {
            "deletedAccessBehavior": "RETURN_NOTHING",
            "unauthorizedAccessBehavior": "RETURN_NOTHING",
            "excludeResultsFilesOutputs": False,
            "wantOutputFiles": False,
            "kernelIds": [],
            "outputFileTypes": [],
            "includeInvalidDataSources": False
        },
        "readMask": "pinnedKernels"
    }
    url = "https://www.kaggle.com/api/i/kernels.KernelsService/ListKernels"
    data = json.dumps(data, separators=(',', ':'))
    kernels = requests.post(url, headers=headers, cookies=cookies, data=data).json()['kernels']

    res = []
    for kernel in kernels:
        temp = {}
        temp['title'] = kernel['title']
        temp['scriptUrl'] = "https://www.kaggle.com" + kernel['scriptUrl']
        res.append(temp)
    res = res[:10]
    return json.dumps(res)


def extract_and_transform_urls(json_urls):
    # 解析 JSON 字符串
    data = json.loads(json_urls)

    # 提取并转换 URL
    urls = []
    for item in data:
        url = item.get("scriptUrl", "")
        match = re.search(r"https://www.kaggle.com/code/(.*)", url)
        if match:
            urls.append(match.group(1))

    return urls




def check_knowledge_base_name(client, knowledge_base_name):
    vector_stores = client.beta.vector_stores.list()
    for vs in vector_stores.data:
        if vs.name == knowledge_base_name:
            return vs.id
    return None


def update_vector_db_mapping(sub_folder_name, vector_db_id):
    # 确保主目录和子目录及其JSON文件存在
    sub_folder_path = create_knowledge_base_folder(sub_folder_name)

    # 获取主目录路径和JSON文件路径
    base_path = os.path.dirname(sub_folder_path)
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')

    # 更新主目录JSON文件
    with open(main_json_file, 'r') as f:
        main_mapping = json.load(f)

    main_mapping[sub_folder_name] = vector_db_id

    with open(main_json_file, 'w') as f:
        json.dump(main_mapping, f, indent=4)

    # 更新子目录JSON文件
    sub_json_file = os.path.join(sub_folder_path, f'{sub_folder_name}_vector_id.json')

    with open(sub_json_file, 'r') as f:
        sub_mapping = json.load(f)

    sub_mapping["vector_db_id"] = vector_db_id

    with open(sub_json_file, 'w') as f:
        json.dump(sub_mapping, f, indent=4)


def create_knowledge_base_folder(sub_folder_name=None):
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')

    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    # 创建 base_path 文件夹
    os.makedirs(base_path, exist_ok=True)

    # 检查并创建主目录 JSON 文件
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        with open(main_json_file, 'w') as f:
            json.dump({}, f, indent=4)

    # 如果 sub_folder_name 不为空，则在 base_path 内创建子文件夹
    if sub_folder_name:
        sub_folder_path = os.path.join(base_path, sub_folder_name)
        os.makedirs(sub_folder_path, exist_ok=True)

        # 检查并创建子目录 JSON 文件
        sub_json_file = os.path.join(sub_folder_path, f'{sub_folder_name}_vector_id.json')
        if not os.path.exists(sub_json_file):
            with open(sub_json_file, 'w') as f:
                json.dump({"vector_db_id": None, "knowledge_base_description": ""}, f, indent=4)

        return sub_folder_path
    else:
        return base_path


def get_specific_files(folder_path):
    # 指定需要过滤的文件扩展名
    file_extensions = ['.md', '.pdf', '.doc', '.docx', '.ppt', '.pptx']

    # 构造文件列表，仅包含特定扩展名的文件
    file_paths = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, file)) and any(file.endswith(ext) for ext in file_extensions)
    ]
    return file_paths


def get_formatted_file_list(folder_path):
    # 检测操作系统
    if os.name == 'posix':  # Unix/Linux/MacOS
        file_path = f'/app/uploads/{folder_path}'
        file_paths = get_specific_files(file_path)
    else:
        file_paths = get_specific_files(folder_path)

    #
    # # Docker
    # file_path = f'/app/uploads/{folder_path}'
    # file_paths = get_specific_files(file_path)
    #
    # # Windows
    # # #  获取指定文件夹内的特定文件类型的文件路径
    # # file_paths = get_specific_files(folder_path)

    # 提取文件名并去掉扩展名
    file_names = [os.path.splitext(os.path.basename(file_path))[0] for file_path in file_paths]

    # 将文件名用顿号分隔并组合成一个字符串
    formatted_file_list = '、'.join(file_names)

    # 构建最终输出字符串
    result = f"当前你的知识库包含文档标题如下：{formatted_file_list}。当用户所提出的问题和你的知识库文档内容相关时，请先检索你的知识库再进行回答。"

    return result


def remove_knowledge_base_info(text):
    keyword = "当前你的知识库包含文档标题如下："

    # 查找关键字的位置
    index = text.find(keyword)

    # 如果关键字存在，删除该关键字及其之后的所有字符
    if index != -1:
        return text[:index]

    # 如果关键字不存在，返回原始字符串
    return text


def clear_folder(folder_path):
    """
    删除指定文件夹内的全部内容
    :param folder_path: 要清空的文件夹路径
    """
    # 检查文件夹是否存在
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # 删除文件夹内的全部内容
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 删除文件或符号链接
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 删除目录
            except Exception as e:
                pass
                # print(f"Failed to delete {file_path}. Reason: {e}")
        # print(f"清空了文件夹: {folder_path}")
    else:
        # print(f"文件夹不存在或不是一个目录: {folder_path}")
        pass


def create_competition_knowledge_base(competition_name, client):
    try:
        load_dotenv()
        headers_json = os.getenv('HEADERS')
        cookies_json = os.getenv('COOKIES')

        headers = json.loads(headers_json)
        cookies = json.loads(cookies_json)

        _id = get_id(keyword=competition_name)

        if _id:
            folder_path = create_kaggle_project_directory(competition_name)
            print(f"已找到指定竞赛{competition_name}，正在检索支持库是否存在竞赛信息...")
            knowledge_base_name = competition_name + '!!' + client.api_key[8:]
            knowledge_base_check = check_knowledge_base_name(client=client, knowledge_base_name=knowledge_base_name)
            if knowledge_base_check:
                user_input = input('检测到存在该赛题知识库，是否更新知识库（1），或者直接使用该知识库（2）：')
                if user_input == '2':
                    return knowledge_base_check
                else:
                    print("即将更新知识库...")
                    # create_knowledge_base(client=client, knowledge_base_name=competition_name)
                    # client.beta.vector_stores.delete(vector_store_id=knowledge_base_check)
                    clear_folder(create_kaggle_project_directory(competition_name))

            print("正在准备构建知识库...")
            create_kaggle_project_directory(competition_name=competition_name)
            overview, data_description = getOverviewAndDescription(_id)
            print("正在获取竞赛说明及数据集说明...")
            overview_md = convert_html_to_markdown(json_to_markdown(overview))
            data_description_md = convert_html_to_markdown(json_to_markdown(data_description))
            save_markdown(content=overview_md, competition_name=competition_name, file_type='overview')
            save_markdown(content=data_description_md, competition_name=competition_name, file_type='data_description')
            print(f"正在获取{competition_name}竞赛热门kernel...")
            json_urls = get_code(_id)
            urls = extract_and_transform_urls(json_urls=json_urls)
            res = download_and_convert_kernels(urls=urls, competition_name=competition_name)
            print("知识文档创建完成，正在进行词向量化处理与存储，请稍后...")
            # home_dir = str(Path.home())
            # folder_path = os.path.join(os.path.expanduser(home_dir), f'.kaggle./{competition_name}_project/knowledge_library')

            # vector_store = client.beta.vector_stores.create(name=knowledge_base_name)
            # file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
            # md_files = [file for file in file_paths if file.endswith('.md')]
            # file_streams = [open(path, "rb") for path in md_files]
            # file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            # vector_store_id=vector_store.id, files=file_streams
            # )
            vector_store_id = create_knowledge_base(client=client, knowledge_base_name=competition_name)
            print("已顺利完成Kaggle竞赛知识库创建，后续可调用知识库回答。")
            return vector_store_id
        else:
            print("找不到对应的竞赛，请检查竞赛名称再试。")
            return None
    except Exception as e:
        print("服务器拥挤，请稍后再试...")
        return None


def python_inter(py_code, g='globals()'):
    """
    专门用于执行python代码，并获取最终查询或处理结果。
    :param py_code: 字符串形式的Python代码，
    :param g: g，字符串形式变量，表示环境变量，无需设置，保持默认参数即可
    :return：代码运行的最终结果
    """
    try:
        # 尝试如果是表达式，则返回表达式运行结果
        return str(eval(py_code, g))
    # 若报错，则先测试是否是对相同变量重复赋值
    except Exception as e:
        global_vars_before = set(g.keys())
        try:
            exec(py_code, g)
        except Exception as e:
            return f"代码执行时报错{e}"
        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        # 若存在新变量
        if new_vars:
            result = {var: g[var] for var in new_vars}
            return str(result)
        else:
            return "已经顺利执行代码"


def sql_inter(sql_query, host, user, password, database, port, g=globals()):
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
        # 执行SQL查询
        result = db_session.execute(sql_query)
        results = result.fetchall()
        # 将结果转换为字典列表
        keys = result.keys()
        results_list = [dict(zip(keys, row)) for row in results]
    finally:
        db_session.close()  # 确保关闭会话

    # 返回 JSON 格式的查询结果
    import json
    return json.dumps(results_list)


def extract_data(sql_query, df_name, host, user, password, database, port, g=globals()):
    """
    借助pymysql将MySQL中的某张表读取并保存到本地Python环境中。
    :param sql_query: 字符串形式的SQL查询语句，用于提取MySQL中的某张表。
    :param df_name: 将MySQL数据库中提取的表格进行本地保存时的变量名，以字符串形式表示。
    :param host: MySQL服务器的主机名
    :param user: MySQL服务器的用户名
    :param password: MySQL服务器的密码
    :param database: MySQL服务器的数据库名
    :param port: MySQL服务器的端口
    :param g: g，字符串形式变量，表示环境变量，无需设置，保持默认参数即可
    :return：表格读取和保存结果
    """

    from sqlalchemy import create_engine
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
    # 创建数据库引擎
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    g[df_name] = pd.read_sql(sql_query, engine)

    return "已成功完成%s变量创建" % df_name


def generate_object_name(base_name="fig", use_uuid=True):
    """
    生成对象名称，可以选择使用UUID或日期时间。

    :param base_name: 基础名称
    :param use_uuid: 是否使用UUID
    :return: 生成的对象名称
    """
    if use_uuid:
        object_name = f"{base_name}_{uuid.uuid4().hex}.png"
    else:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_name = f"{base_name}_{current_time}.png"
    return object_name





def create_knowledge_base_folder(sub_folder_name=None):
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')

    print(f"knowledge_library_path:{knowledge_library_path}")
    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    # 创建 base_path 文件夹
    os.makedirs(base_path, exist_ok=True)

    # 检查并创建主目录 JSON 文件
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        with open(main_json_file, 'w') as f:
            json.dump({}, f, indent=4)

    # 如果 sub_folder_name 不为空，则在 base_path 内创建子文件夹
    if sub_folder_name:
        sub_folder_path = os.path.join(base_path, sub_folder_name)
        os.makedirs(sub_folder_path, exist_ok=True)

        # 检查并创建子目录 JSON 文件
        sub_json_file = os.path.join(sub_folder_path, f'{sub_folder_name}_vector_id.json')
        if not os.path.exists(sub_json_file):
            with open(sub_json_file, 'w') as f:
                json.dump({"vector_db_id": None, "knowledge_base_description": ""}, f, indent=4)

        return sub_folder_path
    else:
        return base_path


def is_folder_not_empty(knowledge_base_name):
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')

    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    # 目标文件夹路径
    target_folder_path = os.path.join(base_path, knowledge_base_name)

    # 检查目标文件夹是否存在
    if not os.path.exists(target_folder_path) or not os.path.isdir(target_folder_path):
        print(f"目标文件夹 {target_folder_path} 不存在或不是一个文件夹。")
        return False

    # 遍历目标文件夹中的文件
    for root, dirs, files in os.walk(target_folder_path):
        for file in files:
            if not file.endswith('.json'):
                return True

    return False






def get_vector_db_id(knowledge_base_name):
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')

    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    # 创建 base_path 文件夹
    os.makedirs(base_path, exist_ok=True)

    # 检查主目录 JSON 文件
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        with open(main_json_file, 'w') as f:
            json.dump({}, f, indent=4)
        return None

    # 读取主目录 JSON 文件
    with open(main_json_file, 'r') as f:
        main_mapping = json.load(f)

    # 检索对应的词向量数据库ID
    vector_db_id = main_mapping.get(knowledge_base_name)

    return vector_db_id


def wait_for_vector_store_ready(vs_id, client, interval=3, max_attempts=20):
    attempt = 0
    while attempt < max_attempts:
        vector_store = client.beta.vector_stores.retrieve(vs_id)
        if vector_store.status == 'completed':
            return True
        time.sleep(interval)
        attempt += 1
    return False


def export_variables():
    return globals()



def reset_base_url(api_key, base_url):
    if is_base_url_valid(api_key, base_url):
        set_key(dotenv_path, 'BASE_URL', base_url)
        print(f"更新后base_url地址：{base_url}")
    else:
        print(f"无效的base_url地址：{base_url}")


def is_base_url_valid(api_key, path):
    original_string = decrypt_string(api_key, key=b'YAboQcXx376HSUKqzkTz8LK1GKs19Skg4JoZH4QUCJc=')
    split_strings = original_string.split(' ')
    s1 = split_strings[0]
    client_tmp = OpenAI(api_key=s1,
                        base_url=path)
    models_tmp = client_tmp.models.list()
    return models_tmp



def delete_all_files(client):
    # 获取所有文件的列表
    files = client.files.list()
    print(files)
    # 逐个删除文件
    for file in files.data:
        file_id = file.id
        client.files.delete(file_id)
    return True


def delete_all_vector_stores(client):
    # 获取所有词向量库的列表
    vector_stores = client.beta.vector_stores.list()
    print(vector_stores)
    # # 逐个删除词向量库
    # for vector_store in vector_stores.data:
    #     vector_store_id = vector_store.id
    #     client.beta.vector_stores.delete(vector_store_id)
    # return True


def delete_all_assistants(client):
    assistants = client.beta.assistants.list()
    for assistant in assistants.data:
        try:
            client.beta.assistants.delete(assistant_id=assistant.id)
            # print(f"Assistant {assistant.id} deleted successfully.")
        except OpenAIError as e:
            print(f"An error occurred while deleting assistant {assistant.id}: {e}")




# def function_to_call(run_details, client, thread_id, run_id):
#     available_functions = {
#         "python_inter": python_inter,
#         "fig_inter": fig_inter,
#         "sql_inter": sql_inter,
#         "extract_data": extract_data,
#         "image_recognition": image_recognition,
#         "get_answer": get_answer,
#         "get_answer_github": get_answer_github,
#     }
#
#     tool_outputs = []
#     tool_calls = run_details.required_action.submit_tool_outputs.tool_calls
#
#     for tool_call in tool_calls:
#         function_name = tool_call.function.name
#         function_args = tool_call.function.arguments
#
#         # 处理多次子调用的情况
#         if function_name == 'multi_tool_use.parallel':
#             tool_uses = json.loads(function_args).get('tool_uses', [])
#             for tool_use in tool_uses:
#                 recipient_name = tool_use.get('recipient_name')
#                 parameters = tool_use.get('parameters')
#
#                 function_to_call = available_functions.get(recipient_name.split('.')[-1])
#
#                 if function_to_call is None:
#                     tool_outputs.append({
#                         "tool_call_id": tool_call.id,
#                         "output": f"函数 {recipient_name} 不存在"
#                     })
#                     continue
#
#                 function_args = json.dumps(parameters)  # 将参数转换为JSON字符串，以便后续处理
#                 function_args = handle_function_args(function_args)
#
#                 if function_args is None:
#                     tool_outputs.append({
#                         "tool_call_id": tool_call.id,
#                         "output": "输入参数不是有效的JSON格式，无法解析"
#                     })
#                     continue
#
#                 # 打印代码
#                 print_code_if_exists(function_args)
#
#                 try:
#                     function_args['g'] = globals()
#                     # 运行外部函数
#                     function_response = function_to_call(**function_args)
#                 except Exception as e:
#                     function_response = "函数运行报错如下:" + str(e)
#
#                 tool_outputs.append({
#                     "tool_call_id": tool_call.id,
#                     "output": function_response
#                 })
#
#         # 处理单个外部函数调用的情况
#         else:
#             function_to_call = available_functions.get(function_name)
#
#             if function_to_call is None:
#                 tool_outputs.append({
#                     "tool_call_id": tool_call.id,
#                     "output": f"函数 {function_name} 不存在"
#                 })
#                 continue
#
#             function_args = handle_function_args(function_args)
#
#             if function_args is None:
#                 tool_outputs.append({
#                     "tool_call_id": tool_call.id,
#                     "output": "输入参数不是有效的JSON格式，无法解析"
#                 })
#                 continue
#
#             # 打印代码
#             print_code_if_exists(function_args)
#
#             try:
#                 function_args['g'] = globals()
#                 # 运行外部函数
#                 function_response = function_to_call(**function_args)
#             except Exception as e:
#                 function_response = "函数运行报错如下:" + str(e)
#
#             tool_outputs.append({
#                 "tool_call_id": tool_call.id,
#                 "output": function_response
#             })
#
#     return tool_outputs