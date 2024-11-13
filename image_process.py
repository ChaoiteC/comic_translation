from PIL import Image, ImageDraw, ImageFont
import os

def add_text_to_image(image_path, text, output_path):
    """
    将提取的文字添加到图片下方，并保存为新的图片
    :param image_path: 原始图片路径
    :param text: 需要添加到图片的文字
    :param output_path: 输出的文件路径
    """
    # 打开图片
    original_image = Image.open(image_path)

    # 创建一个ImageDraw对象来绘制文字
    draw = ImageDraw.Draw(original_image)

    # 指定字体路径，假设字体文件在当前目录的 'fonts' 文件夹下
    font_path = os.path.join(os.getcwd(), 'fonts', 'SourceHanSerifSC-VF.ttf')  # 根据实际路径调整
    try:
        font = ImageFont.truetype(font_path, 24)  # 载入字体，指定字体文件路径
    except IOError:
        font = ImageFont.load_default()  # 如果字体文件不存在，使用默认字体

    # 使用 textbbox 来计算文本的边界框，获取宽度和高度
    text_bbox = draw.textbbox((0, 0), text, font=font)  # 得到文本边界框
    text_width = text_bbox[2] - text_bbox[0]  # 文本宽度
    text_height = text_bbox[3] - text_bbox[1]  # 文本高度

    # 获取图片的尺寸
    width, height = original_image.size

    # 将文字放置在图片下方
    new_height = height + text_height + 10  # 为了留出一些间隔
    new_image = Image.new('RGB', (width, new_height), (255, 255, 255))
    new_image.paste(original_image, (0, 0))

    # 在新的图片上绘制文字
    draw = ImageDraw.Draw(new_image)
    draw.text(((width - text_width) / 2, height + 5), text, font=font, fill=(0, 0, 0))

    # 保存新图片
    new_image.save(output_path)
    print(f"生成的新图片保存为 {output_path}")