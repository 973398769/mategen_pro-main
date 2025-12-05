from collections import defaultdict
from openai import OpenAI  # 确保已导入 OpenAI

def generate_instance_key(enhanced_mode, knowledge_base_chat, knowledge_base_name_id, db_name_id):
    """生成一个基于传入参数的唯一键"""
    return f"{enhanced_mode}-{knowledge_base_chat}-{knowledge_base_name_id}-{db_name_id}"

class CachePool():
    def __init__(self):
        self.assistants = {}
        self.threads = {}
        self.clients = {}
        self.async_clients = {}

    def get_assistant(self, user_id):
        return self.assistants.get(user_id)

    def set_assistant(self, user_id, assistant_id):
        self.assistants[user_id] = assistant_id

    def get_threads(self, assistant_id):
        # 返回与 assistant_id 关联的 thread_id 列表，如果无则返回空列表
        return self.threads.get(assistant_id, [])

    def add_thread(self, assistant_id, thread_id):
        if assistant_id not in self.threads:
            self.threads[assistant_id] = []  # 如果还没有该 assistant_id 的记录，则初始化一个空列表
        if thread_id not in self.threads[assistant_id]:  # 避免重复添加
            self.threads[assistant_id].append(thread_id)  # 添加 thread_id 到列表中

    def thread_exists(self, assistant_id, thread_id):
        # 检查指定的 thread_id 是否存在于对应的 assistant_id 的列表中
        return thread_id in self.get_threads(assistant_id)

    def move_thread_to_end(self, assistant_id, thread_id):
        """
        Move a specified thread_id to the end of the list for a given assistant_id.
        """
        if assistant_id in self.threads:
            thread_list = self.threads[assistant_id]
            if thread_id in thread_list:
                # Remove the thread_id and append it to the end
                thread_list.append(thread_list.pop(thread_list.index(thread_id)))

    def get_client(self, user_id):
        return self.clients.get(user_id)

    def set_client(self, user_id, client_instance):
        if user_id not in self.clients:
            self.clients[user_id] = client_instance  # 直接传递 OpenAI 对象

    def get_async_client(self, user_id):
        return self.async_clients.get(user_id)

    def set_async_client(self, user_id, client_instance):
        if user_id not in self.async_clients:
            self.async_clients[user_id] = client_instance  # 直接传递 OpenAI 对象

    def get_user_resources(self, user_id):
        """
        Retrieve all resources related to a given user ID.
        Returns a dictionary containing the assistant, client, async client, and thread list.
        """
        assistant = self.get_assistant(user_id)
        client = self.get_client(user_id)
        async_client = self.get_async_client(user_id)
        thread_list = self.get_threads(assistant) if assistant else []

        return {
            "assistant_id": assistant,
            "client": client,
            "async_client": async_client,
            "thread_id": thread_list
        }


if __name__ == '__main__':
    # 创建缓存池实例
    cache_pool = CachePool()
