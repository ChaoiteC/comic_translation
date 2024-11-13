import os
from dotenv import load_dotenv
import requests
import base64

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取API Key和Secret Key
client_id = os.getenv('BAIDU_API_KEY')  # 这里从.env文件中获取API Key
client_secret = os.getenv('BAIDU_SECRET_KEY')  # 这里从.env文件中获取Secret Key

# 获取百度API的Access Token
def get_access_token():
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    response = requests.get(url)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print("获取 Access Token 失败！")
        return None

# 发送请求进行图片文字识别
def ocr_image(image_path, access_token):
    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()
        img_base64 = base64.b64encode(img_data).decode('utf-8')

    request_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={access_token}"
    params = {"image": img_base64}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("请求失败:", response.status_code, response.text)
        return None

def parse_result(result):
    if result:
        if "words_result" in result:
            print("识别结果：")
            for item in result["words_result"]:
                print(item["words"])
        else:
            print("未能识别到任何文字。")
    else:
        print("没有返回识别结果。")

# 主程序
if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"
    access_token = get_access_token()
    if access_token:
        result = ocr_image(image_path, access_token)
        parse_result(result)
