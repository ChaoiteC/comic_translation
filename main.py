from BaiduAiOCR import baidu_ai_ocr,get_language_type
from BaiduFanyiOCR import baidufanyi_ocr_translate
from file_selector import select_files
from image_process import save_base64_image
import os
import json

# 主程序
def comic_trans():
    # 打开文件选择窗口，获取图片路径
    image_paths = select_files()
    if not image_paths:
        return
    
    # 用于存储翻译结果的列表
    translation_results = []

    # 遍历每个图片路径进行翻译
    for image_path in image_paths:
        print(f"传递图片: {image_path}")
        # 调用百度翻译OCR
        result = baidufanyi_ocr_translate(image_path, from_lang='jp', to_lang='zh')

        # 将每个翻译结果存储到列表中
        translation_results.append({
            'image_path': image_path,
            'result': result
        })

    # 对 translation_results 进行处理
    for translation in translation_results:
        image_path = translation['image_path']
        result = translation['result']

        # 使用 .get() 方法访问字段，如果字段不存在，返回默认值
        paste_img = result.get("data", {}).get("pasteImg", None)  # 如果"data"字段不存在，返回空字典，避免KeyError

        if paste_img:
            # 获取原始文件名并改变后缀
            file_name = os.path.basename(image_path)  # 获取文件名（不包括路径）
            name, ext = os.path.splitext(file_name)  # 分离文件名和扩展名
            
            # 为新的文件指定新的扩展名（这里可以选择保存为png或者其他格式）
            new_file_name = name + "_translated" + ext

            # 将新文件保存到当前工作目录或指定路径
            output_file = os.path.join(os.path.dirname(image_path), new_file_name)  # 保持在原始路径下保存

            save_base64_image(paste_img, output_file)

if __name__ == "__main__":
    comic_trans()
