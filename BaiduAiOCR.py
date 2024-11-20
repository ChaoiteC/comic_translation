import base64
import requests
import os
import configparser
import json

# 语言类型映射
LANGUAGES = {
    "CHN_ENG": "中英文混合",
    "ENG": "英文",
    "JAP": "日语",
    "KOR": "韩语",
    "FRE": "法语",
    "SPA": "西班牙语",
    "POR": "葡萄牙语",
    "GER": "德语",
    "ITA": "意大利语",
    "RUS": "俄语",
}

def get_language_type():
    """
    交互式选择语言类型
    """
    print("请选择识别语言：")
    for idx, lang in enumerate(LANGUAGES, 1):
        print(f"{idx}. {LANGUAGES[lang]}")
    
    choice = int(input("输入选项（1-10）："))
    selected_lang = list(LANGUAGES.keys())[choice - 1]
    return selected_lang

def baidu_ai_ocr(image_path, language_type = "CHN_ENG", appKey = None, secrctKey = None):

    app_key, secrct_key = check_config('config.ini', appKey, secrctKey)

    access_token = get_access_token(app_key, secrct_key)

    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()
        img_base64 = base64.b64encode(img_data).decode('utf-8')

    request_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={access_token}"
    params = {"image": img_base64,
              "language_type": language_type}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("请求失败:", response.status_code, response.text)
        return None

def check_config(config_path='config.ini', app_key=None, secrct_key=None):
    """
    检查config.ini文件是否存在，且包含[baidu_ai_ocr_api]的api key和secret Key。
    如果app_key或secrct_key为空，要求用户输入并保存。

    参数:
    - config_path: 配置文件路径，默认为'config.ini'
    - app_key: 如果传入了app_key，则使用传入的值
    - secrct_key: 如果传入了secrct_key，则使用传入的值

    返回:
    - 一个字典，包含 'app_key' 和 'secrct_key' 键的配置。
    """
    # 如果 config.ini 文件不存在，创建一个新的配置
    if not os.path.exists(config_path):
        print(f"{config_path} 文件不存在，正在创建新的配置文件。")
        config = configparser.ConfigParser()
        config.add_section('baidu_ai_ocr_api')
        config.set('baidu_ai_ocr_api', 'app_key', '')
        config.set('baidu_ai_ocr_api', 'secrct_key', '')
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # 检查是否有 [baidu_ai_ocr_api] 部分
    if 'baidu_ai_ocr_api' not in config.sections():
        print(f"[baidu_ai_ocr_api] 部分不存在，正在创建该部分。")
        config.add_section('baidu_ai_ocr_api')
        config.set('baidu_ai_ocr_api', 'app_key', '')
        config.set('baidu_ai_ocr_api', 'secrct_key', '')
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    
    # 获取 app_key 和 secrct_key
    app_key_config = config.get('baidu_ai_ocr_api', 'app_key')
    secrct_key_config = config.get('baidu_ai_ocr_api', 'secrct_key')

    # 如果 app_key 或 secrct_key 为空，要求用户输入并更新配置文件
    if not app_key_config or not secrct_key_config:
        print("检测到配置文件中的 app_key 或 secrct_key 为空。")
        if not app_key_config:
            app_key_config = app_key if app_key else input("请输入你的百度AI OCR app_key: ")
        if not secrct_key_config:
            secrct_key_config = secrct_key if secrct_key else input("请输入你的百度AI OCR secrct_key: ")
        
        # 更新配置文件
        config.set('baidu_ai_ocr_api', 'app_key', app_key_config)
        config.set('baidu_ai_ocr_api', 'secrct_key', secrct_key_config)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        
        print("配置已更新。")

    return app_key_config, secrct_key_config

def get_access_token(client_id, client_secret):
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    response = requests.get(url)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print("获取 Access Token 失败。")
        return None
    
if __name__ == "__main__":
    image_path = r'C:\Users\Karub\Desktop\Comic_Trans\test1.jpg'
    
    # 调用ocr_translate函数进行图片翻译
    result = baidu_ai_ocr(image_path)
    
    # 打印翻译结果
    print(json.dumps(result, indent=4, ensure_ascii=False))