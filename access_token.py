import os
from dotenv import load_dotenv
import requests

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取API Key和Secret Key
client_id = os.getenv('BAIDU_API_KEY')  # 这里从.env文件中获取API Key
client_secret = os.getenv('BAIDU_SECRET_KEY')  # 这里从.env文件中获取Secret Key

def get_access_token():
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    response = requests.get(url)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print("获取 Access Token 失败。")
        return None
