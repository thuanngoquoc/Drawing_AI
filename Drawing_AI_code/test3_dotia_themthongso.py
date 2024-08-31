import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import colorchooser
import numpy as np
import cv2

# 1.Chuyển đổi ảnh màu sang ảnh grayscale
img = cv2.imread('E:\My_projects\Git_study\Drawing_AI\Drawing_AI_code\img7.jpg', cv2.IMREAD_UNCHANGED)
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey_img)

# Tạo một hàm để cập nhật ảnh với kích thước Gaussian Blur và các thông số khác
def update_sketch(blur_size, scale_factor):
    blur = cv2.GaussianBlur(invert, (blur_size, blur_size), 0)
    invertedblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(grey_img, invertedblur, scale=scale_factor)
    return sketch

# Khởi tạo ảnh phác thảo với các thông số mặc định
sketch = update_sketch(21, 250.0)
#2.Điều chỉnh kích thước canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=1100, height=1100)
canvas.pack()

# 3.Tạo ngưỡng đen xám
black_threshold = 0  # giá trị ngưỡng đen
gray_upper_bound = 225 # giá trị trên ngưỡng xám
# Điều kiện chọn pixel theo ngưỡng
gray_mask = (sketch >= black_threshold) & (sketch <= gray_upper_bound)
gray_coords = np.column_stack(np.where(gray_mask)) 

stroke_color = tk.StringVar(value="black")  # Màu điểm vẽ
point_size = 5  # Kích thước điểm
delay = 1 # Độ trễ giữa các điểm, tính bằng mili giây
white_pixel_threshold = 240  # Ngưỡng để xác định pixel trắng
collinear_threshold = tk.DoubleVar(value=0.0001)  # Ngưỡng để xác định sự collinear

def is_collinear(p1, p2, p3, threshold):
    # Kiểm tra xem ba điểm có nằm trên cùng một đường thẳng hay không với ngưỡng tùy chỉnh
    return abs((p3[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p3[0] - p1[0])) <= threshold

def reduce_points(coords, threshold):
    reduced_coords = [coords[0]]  # Bắt đầu với điểm đầu tiên
    for i in range(1, len(coords) - 1):
        if not is_collinear(reduced_coords[-1], coords[i], coords[i + 1], threshold):
            reduced_coords.append(coords[i])
    reduced_coords.append(coords[-1])  # Thêm điểm cuối cùng
    return reduced_coords

def draw_points(coords, index=0):
    if index < len(coords):
        point = coords[index]
       
        if sketch[point[0], point[1]] <= white_pixel_threshold:
            x, y = point[1], point[0]  
            canvas.create_oval(x -point_size // 2, y - point_size // 2, x + point_size // 2, y + point_size // 2, fill=stroke_color.get(), outline=stroke_color.get())
        root.after(delay, draw_points, coords, index + 1)

def apply_changes():
    global sketch, gray_coords
    blur_size = int(blur_size_var.get())
    scale_factor = float(scale_factor_var.get())
    
    # Cập nhật ảnh phác thảo với thông số mới
    sketch = update_sketch(blur_size, scale_factor)
    
    # Cập nhật lại các điểm theo ngưỡng mới
    gray_mask = (sketch >= black_threshold) & (sketch <= gray_upper_bound)
    gray_coords = np.column_stack(np.where(gray_mask))
    
    if len(gray_coords) > 0:
        reduced_coords = reduce_points(gray_coords, collinear_threshold.get())
        canvas.delete("all")  # Xóa canvas
        draw_points(reduced_coords)

# Tạo thanh trượt để điều chỉnh kích thước Gaussian Blur
blur_size_var = tk.IntVar(value=21)
blur_slider = tk.Scale(root, from_=1, to=51, label="Gaussian Blur Size", orient="horizontal", variable=blur_size_var, command=lambda x: apply_changes())
blur_slider.pack()

# Tạo thanh trượt để điều chỉnh scale factor
scale_factor_var = tk.DoubleVar(value=250.0)
scale_slider = tk.Scale(root, from_=100.0, to=1000.0, label="Scale Factor", orient="horizontal", resolution=0.1, variable=scale_factor_var, command=lambda x: apply_changes())
scale_slider.pack()

# Tạo thanh trượt để điều chỉnh collinear threshold
collinear_slider = tk.Scale(root, from_=0.0, to=1.0, label="Collinear Threshold", orient="horizontal", resolution=0.01, variable=collinear_threshold, command=lambda x: apply_changes())
collinear_slider.pack()

# Bắt đầu vẽ với thông số mặc định
if len(gray_coords) > 0:
    reduced_coords = reduce_points(gray_coords, collinear_threshold.get())
    draw_points(reduced_coords)

root.mainloop()
