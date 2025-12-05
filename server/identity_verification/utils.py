from server.identity_verification.decryption import decrypt_string
import logging
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from server.utils import find_env_file


# 验证给定的 OpenAI API 密钥是否可以正常访问。
def validate_api_key(api_key: str) -> bool:
    """
    验证给定的 OpenAI API 密钥是否可以正常访问。
    :param api_key: 加密的 API 密钥字符串
    :return: 如果 API 密钥有效且可访问，返回 True；否则返回 False
    """
    if not api_key:
        logging.info(f"API KEY not found")
        return False  # 提取失败，返回 False

    # 加载环境变量
    dotenv_path = find_env_file()  # 调用函数
    load_dotenv(dotenv_path)  # 加载环境变量
    base_url = os.getenv('BASE_URL')

    if base_url == '':
        # 不使用代理
        client = OpenAI(api_key=api_key)
    else:
        # 使用代理
        client = OpenAI(api_key=api_key, base_url=base_url)
    try:
        # 尝试调用 OpenAI API 来验证 API 密钥，设置超时
        client.models.list(timeout=5)  # 5秒超时
        return True  # 如果成功，返回 True
    except OpenAIError as e:
        logging.error(f"PI error: {e}")
        return False  # 如果发生错误，返回 False
