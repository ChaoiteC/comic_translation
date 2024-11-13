import tkinter as tk
from tkinter import filedialog

def select_image_files():
    """选择多个图片文件"""
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口
    file_paths = filedialog.askopenfilenames(
        title="选择图片文件",
        filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp"), ("All files", "*.*"))
    )
    return file_paths
