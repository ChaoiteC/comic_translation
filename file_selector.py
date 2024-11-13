import tkinter as tk
from tkinter import filedialog
import sys

def select_image_files():
    """选择多个图片文件（支持图形界面和命令行回退）"""
    if sys.platform == "win32" or sys.platform == "darwin" or sys.platform == "linux":
        try:
            # 使用tkinter的文件对话框选择文件
            root = tk.Tk()
            root.withdraw()  # 不显示主窗口
            file_paths = filedialog.askopenfilenames(
                title="选择需要翻译的图片文件",
                filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp"), ("All files", "*.*"))
            )
            return file_paths
        except Exception as e:
            print(f"无法弹出文件选择对话框：{e}")
            return []
    else:
        # 如果是命令行环境，提供命令行输入路径的方式
        file_paths = input("请输入图片文件路径，以逗号分隔：").split(",")
        return [path.strip() for path in file_paths]
