import base64
import requests

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
