from access_token import get_access_token
from ocr import ocr_image
from file_selector import select_image_files
from image_process import add_text_to_image
import os

# 主程序
def main():
    # 打开文件选择窗口，获取图片路径
    image_paths = select_image_files()
    if not image_paths:
        print("没有选择图片文件。")
        return

    # 获取Access Token
    access_token = get_access_token()
    if not access_token:
        print("无法获取Access Token。")
        return
    
    # 批量处理每个图片文件
    for image_path in image_paths:
        """处理 OCR 请求"""
        result = ocr_image(image_path, access_token)
        if not result or "words_result" not in result:
            print(f"无法识别图片 {image_path}")
            return
        # 获取识别的文字
        text = "\n".join([item["words"] for item in result["words_result"]])

        # 设置输出文件路径
        output_path = os.path.splitext(image_path)[0] + "_with_text.jpg"

        # 添加文字并保存新图片
        add_text_to_image(image_path, text, output_path)
        
        

if __name__ == "__main__":
    main()
