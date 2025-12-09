import os
import requests
import json
from dotenv import load_dotenv, set_key, find_dotenv
from IPython.display import display, Code, Markdown, Image
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

# Google search test
def test_google_search_api(search_term='openai'):
    """
    Test whether Google Search API can connect smoothly and get a response normally.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    google_search_key = os.getenv('GOOGLE_SEARCH_KEY')
    cse_id = os.getenv('CSE_ID')
    
    params = {
        'q': search_term,
        'key': google_search_key,
        'cx': cse_id
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Request failed, HTTP status code: {response.status_code}")
            return False
        
        data = response.json()
        if 'items' in data:
            print("Test successful: API response contains expected data.")
            return True
        else:
            print("Test failed: API response does not contain expected data.")
            return False
    
    except Exception as e:
        print(f"Test failed: Exception occurred - {e}")
        return False
    
def write_google_env(google_search_key, cse_id):
    """
    Write google_search_key and cse_id to the .env file in the current project folder as environment variables.
    """
    # Load .env file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(BASE_DIR, '.env')
    # Load .env file, create one if it doesn't exist
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w') as f:
            pass  # Create an empty .env file
        
    load_dotenv(dotenv_path)
    
    if load_dotenv(dotenv_path):
    
        set_key(dotenv_path, 'GOOGLE_SEARCH_KEY', google_search_key)
        set_key(dotenv_path, 'CSE_ID', cse_id)
        
        print(f".env file updated: GOOGLE_SEARCH_KEY={google_search_key}, CSE_ID={cse_id}")
    else:
        print("Cannot find configuration file, please write configuration file first")
        return None
    

# Zhihu crawler test  
def test_spider_response(test_url='https://www.zhihu.com/question/589955237'):
    """
    Test whether a crawler response is smooth.
    """
    cookie = os.getenv('ZHIHU_SEARCH_COOKIE')
    user_agent = os.getenv('ZHIHU_SEARCH_USER_AGENT')
    
    if not cookie or not user_agent:
        print("Environment variable ZHIHU_SEARCH_COOKIE or ZHIHU_SEARCH_USER_AGENT not set")
        return False
    
    # Build request headers
    headers = {
        'authority': 'www.zhihu.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent,
    }

    try:
        # Send GET request
        response = requests.get(test_url, headers=headers)
        
        # Check if HTTP status code is 200 (OK)
        if response.status_code == 200:
            print("Test successful: Crawler response normal.")l: Crawler response normal.")
            return True
        else:
            print(f"Test failed, HTTP status code: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"Test failed: Exception occurred - {e}")
        return False

def write_zhihu_env(cookie, user_agent):
    """
    Write ZHIHU_SEARCH_COOKIE and ZHIHU_SEARCH_USER_AGENT to the .env file in the current project folder as environment variables.
    """
    # Load .env file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(BASE_DIR, '.env')
    # Load .env file, create one if it doesn't exist
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w') as f:
            pass  # Create an empty .env file
        
    load_dotenv(dotenv_path)
    
    if load_dotenv(dotenv_path):
        set_key(dotenv_path, 'ZHIHU_SEARCH_COOKIE', cookie)
        set_key(dotenv_path, 'ZHIHU_SEARCH_USER_AGENT', user_agent)      
        print(f".env file updated: ZHIHU_SEARCH_COOKIE={cookie}, ZHIHU_SEARCH_USER_AGENT={user_agent}")
        
    else:
        print("Cannot find configuration file, please write configuration file first")
        return None

# Github connection test
def test_github_token(owner="THUDM", repo="P-tuning-v2"):
    """
    Test whether GitHub token can be used normally.
    """
    
    github_token = os.getenv('GITHUB_TOKEN')
    user_agent = os.getenv('ZHIHU_SEARCH_USER_AGENT')
    # Build request headers
    headers = {
        "Authorization": f"token {github_token}",
        "User-Agent": user_agent
    }

    # Build request URL
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    try:
        # Send GET request
        response = requests.get(url, headers=headers)
        
        # Check if HTTP status code is 200 (OK)
        if response.status_code == 200:
            print("Test successful: GitHub token working normally.")
            return True
        else:
            print(f"Test failed, HTTP status code: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"Test failed: Exception occurred - {e}")
        return False
    
def write_github_token_to_env(github_token):
    """
    Write GitHub token to the .env file in the current project folder as an environment variable.
    """
    # Load .env file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(BASE_DIR, '.env')
    # Load .env file, create one if it doesn't exist
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w') as f:
            pass  # Create an empty .env file
        
    load_dotenv(dotenv_path)
    
    # If .env file doesn't exist, create one
    if load_dotenv(dotenv_path):
        set_key(dotenv_path, 'GITHUB_TOKEN', github_token)

        print(f".env file updated: GITHUB_TOKEN={github_token}")
    else:
        print("Cannot find configuration file, please write configuration file first")
        return None
       
# Alibaba Cloud configuration
def test_oss_api():
    """
    Test whether Alibaba Cloud OSS API can be called normally.
    """
    access_key_id = os.getenv('ACCESS_KEY_ID')
    access_key_secret = os.getenv('ACCESS_KEY_SECRET')
    endpoint = os.getenv('ENDPOINT')
    bucket_name = os.getenv('BUCKET_NAME')
    
    if access_key_id or access_key_secret or endpoint or bucket_name == None:
        print("Please set related variable values first")
        return False
    
    try:
        # Initialize OSS client
        
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)

        # Test listing all files in the storage space
        file_list = list(oss2.ObjectIterator(bucket))
        
        print(f"Test successful: Listed files in storage space, total {len(file_list)} files.")
        return True
    
    except OssError as e:
        print(f"Test failed: OSS API call failed - {e}")
        return False
    
def write_oss_env(access_key_id, access_key_secret, endpoint, bucket_name):
    """
    Write Alibaba Cloud OSS related variables to the .env file in the current project folder as environment variables.
    """
    # Load .env file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(BASE_DIR, '.env')
    # Load .env file, create one if it doesn't exist
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w') as f:
            pass  # Create an empty .env file

    load_dotenv(dotenv_path)
    
    if load_dotenv(dotenv_path):
        set_key(dotenv_path, 'OSS_ACCESS_KEY_ID', access_key_id)
        set_key(dotenv_path, 'OSS_ACCESS_KEY_SECRET', access_key_secret)
        set_key(dotenv_path, 'OSS_ENDPOINT', endpoint)
        set_key(dotenv_path, 'OSS_BUCKET_NAME', bucket_name)

        print(f".env file updated: OSS_ACCESS_KEY_ID={access_key_id}, OSS_ACCESS_KEY_SECRET={access_key_secret}, OSS_ENDPOINT={endpoint}, OSS_BUCKET_NAME={bucket_name}")
    else:
        print("Cannot find configuration file, please write configuration file first")
        return None

# Kaggle configuration    
def test_kaggle_api():
    """
    Test whether Kaggle API can connect.

    :return: Test result (True indicates success, False indicates failure)
    """
    # Load environment variables
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    headers_json = os.getenv('HEADERS')
    cookies_json = os.getenv('COOKIES')
    
    if not headers_json or not cookies_json:
        print("Environment variable HEADERS or COOKIES not set")
        return False

    # Parse JSON string to dictionary
    headers = json.loads(headers_json)
    cookies = json.loads(cookies_json)
    
    url = "https://www.kaggle.com/api/i/search.SearchWebService/FullSearchWeb"
    data = {
        "query": 'titanic',
        "page": 1,
        "resultsPerPage": 20,
        "showPrivate": True
    }
    data = json.dumps(data, separators=(',', ':'))

    try:
        # Send POST request
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        
        # Check if response is successful
        if response.status_code == 200:
            response_data = response.json()
            print("Test successful: Kaggle API response normal.")
            return True
        else:
            print(f"Test failed, HTTP status code: {response.status_code}")
            return False

    except Exception as e:
        print(f"Test failed: Exception occurred - {e}")
        return False    
    
def write_kaggle_env(headers, cookies):
    """
    Write HEADERS and COOKIES to the .env file in the current project folder as environment variables.
    """
    # Load .env file
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(BASE_DIR, '.env')
    # Load .env file, create one if it doesn't exist
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w') as f:
            pass  
    
    load_dotenv(dotenv_path)
    
    # If .env file doesn't exist, create one
    if load_dotenv(dotenv_path):
        set_key(dotenv_path, 'HEADERS', headers)
        set_key(dotenv_path, 'COOKIES', cookies)

        print(f".env file updated: HEADERS={headers}, COOKIES={cookies}")    
    else:
        print("Cannot find configuration file, please write configuration file first")
        return None        
    

# Print document   
def fetch_and_display_markdown(url):
    """
    Get document content from specified URL and print in Markdown format.
    """
    try:
        # Send GET request to get document content
        response = requests.get(url)
        
        # Check if HTTP status code is 200 (OK)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            content = response.text
            
            # Print content in Markdown format
            display(Markdown(content))
        else:
            print(f"Failed to get document, HTTP status code: {response.status_code}")
    
    except Exception as e:
        print(f"Failed to get document: Exception occurred - {e}")