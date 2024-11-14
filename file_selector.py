import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os

def is_valid_image(file_path):
    """
    检查文件是否符合要求：
    - 格式必须是 jpg, jpeg, 或 png（小写）
    - 文件大小不超过 4MB
    - 最短边至少 30px，最长边最大 4096px
    - 长宽比不超过 3:1

    参数:
    - file_path: 图片文件路径
    
    返回:
    - 如果图片符合要求，返回 True，否则返回 False
    """
    # 检查文件格式（小写）
    if not file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        return False
    
    # 检查文件大小（最大 4MB）
    if os.path.getsize(file_path) > 4 * 1024 * 1024:
        return False
    
    try:
        # 使用PIL打开图片，获取尺寸
        with Image.open(file_path) as img:
            width, height = img.size
            
            # 检查最短边至少为30px，最长边最大4096px
            if min(width, height) < 30 or max(width, height) > 4096:
                return False
            
            # 检查长宽比（宽/高 <= 3）
            if max(width, height) / min(width, height) > 3:
                return False

    except Exception as e:
        # 如果无法打开图片，返回 False
        print(f"无法处理文件 {file_path}: {e}")
        return False

    # 如果图片符合所有要求，返回 True
    return True

def select_files():
    """
    拉起系统文件选择窗口，返回符合条件的图片文件路径列表。
    支持格式：.jpg, .jpeg, .png，且图片符合大小和尺寸要求。
    
    返回:
    - 合格的图片文件路径列表，如果有不符合条件的图片，输出信息并返回空列表。
    """
    # 打开文件选择对话框，允许选择多个文件
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_paths = filedialog.askopenfilenames(
        title="选择图片文件",
        filetypes=[("图片文件", "*.jpg;*.jpeg;*.png")]  # 只允许选择jpg, jpeg, png文件
    )
    
    valid_files = []
    invalid_files = []  # 用于记录不符合条件的文件

    # 遍历选中的文件路径
    for file_path in file_paths:
        if is_valid_image(file_path):
            valid_files.append(file_path)
        else:
            invalid_files.append(file_path)
    
    # 如果有不符合条件的文件，输出信息
    if invalid_files:
        print("以下图片不符合要求：")
        for invalid in invalid_files:
            print(f"{invalid}: 不符合格式、尺寸、大小或长宽比要求")
    
    # 如果有不符合条件的图片，返回空列表
    if invalid_files:
        return []

    return valid_files

# 调用函数并输出符合条件的文件路径
if __name__ == "__main__":
    valid_images = select_files()
    if valid_images:
        print("符合条件的图片文件:")
        for image in valid_images:
            print(image)
    else:
        print("没有符合条件的图片。")
