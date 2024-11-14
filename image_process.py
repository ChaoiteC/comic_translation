import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO

def blur_image(image, rect, blur_radius=15):
    """
    对图像中的指定矩形区域进行模糊处理
    :param image: 原图像
    :param rect: 要模糊的区域 (left, top, width, height)
    :param blur_radius: 模糊半径
    :return: 模糊处理后的图像
    """
    # 获取矩形区域
    x, y, w, h = rect
    cropped_img = image[y:y+h, x:x+w]
    
    # 对该区域进行模糊处理
    blurred_cropped_img = cv2.GaussianBlur(cropped_img, (blur_radius, blur_radius), 0)
    
    # 将模糊后的区域放回原图
    image[y:y+h, x:x+w] = blurred_cropped_img
    return image

def overlay_text_on_image(image_path, translation_result):
    """
    对图像进行模糊处理，并覆盖翻译文本
    - param image_path: 图片路径
    - param translation_result: 翻译结果，包括文本位置和翻译内容
    - return: 最终的图像
    """
    # 加载图像
    image = cv2.imread(image_path)
    
    # 获取字体
    font = ImageFont.load_default()  # 这里可以使用自定义字体
    pil_image = Image.open(image_path)
    draw = ImageDraw.Draw(pil_image)
    
    # 遍历翻译内容
    for content in translation_result.get('content', []):
        # 获取翻译文本
        src_text = content.get('src', '')
        dst_text = content.get('dst', '')
        rect = content.get('rect', [])
        
        if not rect or not dst_text:
            continue
        
        # 1. 模糊处理区域
        # rect 是左上角坐标、宽高，我们需要将其转化为 (x, y, w, h) 格式
        x, y, w, h = rect
        image = blur_image(image, (x, y, w, h))
        
        # 2. 在图像上覆盖翻译文本
        # 在原图上绘制翻译文本
        draw.text((x, y), dst_text, font=font, fill=(255, 255, 255))
    
    # 转换回 OpenCV 格式的图像
    final_image = np.array(pil_image)
    
    # 保存或显示图像
    output_image_path = "translated_image.jpg"
    cv2.imwrite(output_image_path, final_image)
    return output_image_path

def save_base64_image(base64_data, output_file):
    """
    将base64编码的数据解码并保存为图片文件
    - param base64_data: base64编码的字符串
    - param output_file: 保存的图片文件路径
    """
    # 解码base64数据
    image_data = base64.b64decode(base64_data)

    # 将解码后的数据保存为图片文件
    with open(output_file, 'wb') as img_file:
        img_file.write(image_data)

    print(f"图片已保存为: {output_file}")
