from access_token import get_access_token
from ocr import ocr_image,get_language_type
from baidufanyi_ocr import baidufanyi_ocr_translate
from file_selector import select_files
from image_process import add_text_to_image
import os
import json

# 主程序
def comic_trans():
    # 打开文件选择窗口，获取图片路径
    image_paths = select_files()
    if not image_paths:
        return
    
    # 遍历传入图片
    for image in image_paths:
        print(f"翻译图片: {image}")
        # 调用百度翻译OCR
        result = baidufanyi_ocr_translate(image, from_lang='zh', to_lang='en')
        print(f"翻译结果: {json.dumps(result, indent=4, ensure_ascii=False)}")
        
        

if __name__ == "__main__":
    comic_trans()
