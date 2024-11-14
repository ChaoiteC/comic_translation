# -*- coding: utf-8 -*-
import configparser
import requests
import random
import json
import os
from hashlib import md5

def baidufanyi_ocr_translate(image_path, from_lang='zh', to_lang='en', appid=None, appkey=None):
    """
    使用百度翻译API对给定的图片进行OCR翻译，并返回翻译结果。
    
    参数:
    - image_path: 图片文件的路径
    - from_lang: 原语言，默认为简体中文（'zh'）
    - to_lang: 目标语言，默认为英语（'en'）

    返回:
    - JSON格式的翻译结果
    """
    
    # 百度API的端点和路径
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/sdk/picture'
    url = endpoint + path

    # 从config.ini获取 id 与 key
    check_and_update_config('config.ini', appid, appkey)
    app_id, app_key = load_config('config.ini')
    
    # 生成盐值salt和签名sign
    salt = random.randint(32768, 65536)  # 随机生成salt
    sign = get_md5(app_id + get_file_md5(image_path) + str(salt) + 'APICUID' + 'mac' + app_key)  # 生成签名
    
    # 构造请求参数
    payload = {
        'from': from_lang,  # 来源语言
        'to': to_lang,      # 目标语言
        'appid': app_id,     # 应用ID
        'salt': salt,        # 随机盐值
        'sign': sign,        # 签名
        'cuid': 'APICUID',
        'mac': 'mac'
    }
    
    # 读取图片文件并构建文件字典
    image = {'image': (os.path.basename(image_path), open(image_path, 'rb'), "multipart/form-data")}
    
    # 发送POST请求
    response = requests.post(url, params=payload, files=image)
    
    # 解析返回的JSON响应
    result = response.json()
    
    # 返回翻译结果
    return result


def get_md5(string, encoding='utf-8'):
    """
    计算字符串的MD5值

    参数:
    - string: 要计算MD5的字符串
    - encoding: 字符串的编码方式，默认为utf-8

    返回:
    - MD5的十六进制字符串
    """
    return md5(string.encode(encoding)).hexdigest()


def get_file_md5(file_name):
    """
    计算文件的MD5值

    参数:
    - file_name: 文件的路径

    返回:
    - 文件内容的MD5值（十六进制）
    """
    with open(file_name, 'rb') as f:
        data = f.read()
        return md5(data).hexdigest()

def load_config(config_path='config.ini'):
    """
    读取配置文件并返回配置字典。
    
    参数:
    - config_path: 配置文件路径，默认为 config.ini。
    
    返回:
    - 返回包含配置项的字典。
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # 获取 baidu_api 节下的配置项
    app_id = config.get('baidufanyi_ocr_api', 'appid')
    app_key = config.get('baidufanyi_ocr_api', 'appkey')

    return app_id, app_key

def check_and_update_config(config_path='config.ini', appid=None, appkey=None):
    """
    检查config.ini文件是否存在，且包含[baidufanyi_ocr_api]的app_id和app_key。
    如果appid或appkey为空，要求用户输入并保存。

    参数:
    - config_path: 配置文件路径，默认为'config.ini'
    - appid: 如果传入了app_id，则使用传入的值
    - appkey: 如果传入了app_key，则使用传入的值

    返回:
    - 一个字典，包含 'appid' 和 'appkey' 键的配置。
    """
    # 如果 config.ini 文件不存在，创建一个新的配置
    if not os.path.exists(config_path):
        print(f"{config_path} 文件不存在，正在创建新的配置文件。")
        config = configparser.ConfigParser()
        config.add_section('baidufanyi_ocr_api')
        config.set('baidufanyi_ocr_api', 'appid', '')
        config.set('baidufanyi_ocr_api', 'appkey', '')
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # 检查是否有 [baidufanyi_ocr_api] 部分
    if 'baidufanyi_ocr_api' not in config.sections():
        print(f"[baidufanyi_ocr_api] 部分不存在，正在创建该部分。")
        config.add_section('baidufanyi_ocr_api')
        config.set('baidufanyi_ocr_api', 'appid', '')
        config.set('baidufanyi_ocr_api', 'appkey', '')
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    
    # 获取 appid 和 appkey
    appid_config = config.get('baidufanyi_ocr_api', 'appid')
    appkey_config = config.get('baidufanyi_ocr_api', 'appkey')

    # 如果 appid 或 appkey 为空，要求用户输入并更新配置文件
    if not appid_config or not appkey_config:
        print("检测到配置文件中的 appid 或 appkey 为空。")
        if not appid_config:
            appid_config = appid if appid else input("请输入你的百度翻译 API appid: ")
        if not appkey_config:
            appkey_config = appkey if appkey else input("请输入你的百度翻译 API appkey: ")
        
        # 更新配置文件
        config.set('baidufanyi_ocr_api', 'appid', appid_config)
        config.set('baidufanyi_ocr_api', 'appkey', appkey_config)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        
        print("配置已更新。")

    return {'appid': appid_config, 'appkey': appkey_config}

# 示例：如何调用ocr_translate函数
if __name__ == "__main__":
    image_path = r'C:\Users\Karub\Desktop\Comic_Trans\test1.jpg'  # 这里填写你要翻译的图片路径
    
    # 调用ocr_translate函数进行图片翻译
    result = baidufanyi_ocr_translate(image_path)
    
    # 打印翻译结果
    print(json.dumps(result, indent=4, ensure_ascii=False))
