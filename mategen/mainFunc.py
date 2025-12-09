from IPython.display import display, Code, Markdown, Image
from IPython import get_ipython
import time
import openai
import os
import json
from openai import OpenAI
from openai import OpenAIError
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime
from pathlib import Path
import oss2
from dotenv import load_dotenv, set_key, find_dotenv
import pymysql
import io
import uuid
import re
import glob
import shutil
import inspect
import requests
import random
import string
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
from bs4 import BeautifulSoup
import dateutil.parser as parser
import tiktoken
from lxml import etree
import sys
from cryptography.fernet import Fernet
import numpy as np
import pandas as pd
import html2text
import subprocess
import zipfile
import nbconvert
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(f"BASE_DIR: {BASE_DIR}")
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
# print(f"dotenv_path: {dotenv_path}")

def clean_and_convert_to_json(raw_str):
    """
    Clean and convert irregular strings to JSON format-compliant strings
    :param raw_str: Irregular raw string
    :return: JSON formatted string or error message
    """
    # Replace unescaped newlines
    cleaned_str = re.sub(r'\\n', r'\\\\n', raw_str)
    # Replace unescaped single quotes
    cleaned_str = re.sub(r'(?<!\\)\'', r'\"', cleaned_str)
    # Replace unescaped backslashes
    cleaned_str = re.sub(r'\\(?=\W)', r'\\\\', cleaned_str)
        
    # Try to convert the cleaned string to a JSON object
    json_obj = json.loads(cleaned_str)
    # Format JSON object as string
    json_str = json.dumps(json_obj, indent=2, ensure_ascii=False)
    return json_str

def clear_folder(path):
    """
    Clear all files and subfolders under the specified path.
    
    :param path: The folder path to clear.
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
    Process function arguments, check and convert to JSON format
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
    Print code if code snippet exists
    """
    def convert_to_markdown(code, language):
        return f"```{language}\n{code}\n```"
    
    # If SQL, print code in Markdown SQL format
    if function_args.get('sql_query'):
        code = function_args['sql_query']
        markdown_code = convert_to_markdown(code, 'sql')
        print("About to execute the following code:")
        display(Markdown(markdown_code))

    # If Python, print code in Markdown Python format
    elif function_args.get('py_code'):
        code = function_args['py_code']
        markdown_code = convert_to_markdown(code, 'python')
        print("About to execute the following code:")
        display(Markdown(markdown_code))


def extract_run_id(text):
    pattern = r'run_\w+'  # Regular expression pattern to match characters starting with run_
    match = re.search(pattern, text)
    if match:
        return match.group(0)  # Return matched string
    else:
        return None
    