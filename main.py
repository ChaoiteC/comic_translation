from access_token import get_access_token, client_id, client_secret
from ocr import ocr_image
from file_selector import select_image_file
import os

# 主程序
def main():
    # 打开文件选择窗口，获取图片路径
    image_path = select_image_file()
    if not image_path:
        print("没有选择图片文件")
        return

    # 获取Access Token
    access_token = get_access_token()
    if not access_token:
        print("无法获取Access Token")
        return
    
    # 解析并显示结果
    result = ocr_image(image_path, access_token)
    if result:
        if "words_result" in result:
            print("识别结果：")
            for item in result["words_result"]:
                print(item["words"])
        else:
            print("未能识别到任何文字。")
    else:
        print("没有返回识别结果。")


if __name__ == "__main__":
    main()
