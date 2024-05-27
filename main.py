"""
作者：[赵泽霖]
联系方式：[zhaozelinz@126.com]
版权所有 (c) [2024] [赵泽霖]

[您的简要版权声明或版权声明链接]
本项目地址:https://github.com/ZhaoZelin2000/PDF-Separator-color-and-black-white-pages
本代码修改自:https://github.com/RicePasteM/Color-BW-Separator-for-PDF/tree/master


-------------------------------------------------------------

Author: [Zelin Zhao]
Contact: [zhaozelinz@126.com]
Copyright (c) [2024] [Zelin Zhao]

[Your brief copyright statement or copyright statement link]

Other information or notes...
本项目地址:https://github.com/ZhaoZelin2000/PDF-Separator-color-and-black-white-pages
本代码修改自:https://github.com/RicePasteM/Color-BW-Separator-for-PDF/tree/master
"""













import pymupdf as fitz
import numpy as np
import os
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, messagebox


def is_color_image(image, saturation_threshold=0.35, color_fraction_threshold=0.001):
    image = image.convert('RGB')
    pixels = np.array(image) / 255.0  # 归一化像素值到[0,1]范围

    # 将RGB转换为HSV
    max_rgb = np.max(pixels, axis=2)
    min_rgb = np.min(pixels, axis=2)
    delta = max_rgb - min_rgb

    # 饱和度
    saturation = delta / (max_rgb + 1e-7)  # 防止除以零

    # 判断饱和度大于阈值的彩色像素
    color_pixels = saturation > saturation_threshold
    color_fraction = np.mean(color_pixels)

    return color_fraction > color_fraction_threshold


def is_color_page(page):
    """
    Check if a page is a color page.
    """
    # Render page to a pixmap
    pix = page.get_pixmap()
    # Convert pixmap to an image
    img = pix.tobytes("png")


    # Create an image object using PIL
    from PIL import Image
    from io import BytesIO
    image = Image.open(BytesIO(img))

    return is_color_image(image)


def split_pdf(input_pdf_path, output_color_pdf_path, output_bw_pdf_path, is_double_sized_printing):
    # Open the input PDF
    doc = fitz.open(input_pdf_path)

    # Create new PDFs for color and black & white pages
    color_doc = fitz.open()
    bw_doc = fitz.open()

    # Save color and bw pages number
    color_pages = []
    bw_pages = []

    # Iterate over each page in the input PDF
    for page_num in tqdm(range(len(doc))):
        page = doc.load_page(page_num)

        # Check if the page is a color page
        if is_color_page(page):
            color_pages.append(page_num)

    # Handle double sized printing
    if is_double_sized_printing:
        for page_num in color_pages:
            if page_num % 2 == 0 and page_num + 1 not in color_pages and page_num + 1 < len(doc):
                color_pages.append(page_num + 1)
            if page_num % 2 == 1 and page_num - 1 not in color_pages and page_num - 1 > 0:
                color_pages.append(page_num - 1)

    # Insert BW Pages
    for page_num in range(len(doc)):
        if page_num not in color_pages:
            bw_pages.append(page_num)

    # Insert PDF pages
    if color_pages:
        for page_num in sorted(color_pages):
            color_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    
    if bw_pages:
        for page_num in sorted(bw_pages):
            bw_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

    # Save the new PDFs
    print(f"Output color PDF path: {output_color_pdf_path}")  # 调试语句
    print(f"Output BW PDF path: {output_bw_pdf_path}")  # 调试语句
    if color_pages:
        color_doc.save(output_color_pdf_path)
    if bw_pages:
        bw_doc.save(output_bw_pdf_path)

    # Close all documents
    doc.close()
    color_doc.close()
    bw_doc.close()

# if __name__ == '__main__':
#     INPUT_PDF_PATH = 'example.pdf'  # 待转换的PDF路径
#     OUTPUT_DIR = './output'  # 输出文件夹
#     OUTPUT_COLOR_PDF_PATH = os.path.join(OUTPUT_DIR, 'color_pages.pdf')  # 彩色部分PDF输出路径
#     OUTPUT_BW_PDF_PATH = os.path.join(OUTPUT_DIR, 'bw_pages.pdf')  # 黑白部分PDF输出路径
#     IS_DOUBLE_SIZED_PRINTING = True  # 是否双面打印
    
#     # Create the output directory if it doesn't exist
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
  

#     split_pdf(INPUT_PDF_PATH, OUTPUT_COLOR_PDF_PATH, OUTPUT_BW_PDF_PATH, IS_DOUBLE_SIZED_PRINTING)

    
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def select_print_option():
    def on_select():
        print_option_window.is_double_sized_printing = (print_option.get() == 'double')
        print_option_window.destroy()

    print_option_window = tk.Toplevel()
    print_option_window.title("Select Print Option")

    print_option = tk.StringVar(value='single')

    tk.Label(print_option_window, text="Select Print Option:").pack(anchor=tk.W)

    tk.Radiobutton(print_option_window, text="Single-sided", variable=print_option, value='single').pack(anchor=tk.W)
    tk.Radiobutton(print_option_window, text="Double-sided", variable=print_option, value='double').pack(anchor=tk.W)

    tk.Button(print_option_window, text="OK", command=on_select).pack()

    # Center the window
    center_window(print_option_window)

    print_option_window.is_double_sized_printing = False
    print_option_window.grab_set()
    print_option_window.wait_window()

    return print_option_window.is_double_sized_printing

def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    input_pdf_paths = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
    if not input_pdf_paths:
        messagebox.showerror("Error", "No files selected")
        return

    output_dir = filedialog.askdirectory(title="Select output directory")
    if not output_dir:
        messagebox.showerror("Error", "No output directory selected")
        return

    # Show the print option selection dialog
    is_double_sized_printing = select_print_option()

    for input_pdf_path in input_pdf_paths:
        file_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
        output_color_pdf_path = os.path.join(output_dir, f'{file_name}_color_pages.pdf')
        output_bw_pdf_path = os.path.join(output_dir, f'{file_name}_bw_pages.pdf')

        try:
            split_pdf(input_pdf_path, output_color_pdf_path, output_bw_pdf_path, is_double_sized_printing)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing {input_pdf_path}: {str(e)}")
            continue

    messagebox.showinfo("Success", "PDF files processed successfully")

if __name__ == '__main__':
    print("""
    作者：赵泽霖
    联系方式：zhaozelinz@126.com
    版权所有 (c) 2024 赵泽霖

    [您的简要版权声明或版权声明链接]
    本项目地址: https://github.com/ZhaoZelin2000/PDF-Separator-color-and-black-white-pages
    本代码修改自: https://github.com/RicePasteM/Color-BW-Separator-for-PDF/tree/master
    """)

    select_files()