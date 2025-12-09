from server.identity_verification.decryption import decrypt_string
import logging
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from server.utils import find_env_file


# Validate whether the given OpenAI API key can be accessed normally
def validate_api_key(api_key: str) -> bool:
    """
    Validate whether the given OpenAI API key can be accessed normally.
    :param api_key: Encrypted API key string
    :return: Returns True if API key is valid and accessible; otherwise returns False
    """
    if not api_key:
        logging.info(f"API KEY not found")
        return False  # Extraction failed, return False

    # Load environment variables
    dotenv_path = find_env_file()  # Call function
    load_dotenv(dotenv_path)  # Load environment variables
    base_url = os.getenv('BASE_URL')

    if base_url == '':
        # Don't use proxy
        client = OpenAI(api_key=api_key)
    else:
        # Use proxy
        client = OpenAI(api_key=api_key, base_url=base_url)
    try:
        # Try calling OpenAI API to validate API key, set timeout
        client.models.list(timeout=5)  # 5 second timeout
        return True  # If successful, return True
    except OpenAIError as e:
        logging.error(f"PI error: {e}")
        return False  # If an error occurs, return False
