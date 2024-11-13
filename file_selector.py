import tkinter as tk
from tkinter import filedialog

# 通过Windows选择图片
def select_image_file():
    root = tk.Tk()
    root.withdraw()  # 不显示主窗口
    file_path = filedialog.askopenfilename(
        title="选择图片文件",
        filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp"), ("All files", "*.*"))
    )
    return file_path
