import base64
import requests

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

def ocr_image(image_path, language_type, access_token):
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
