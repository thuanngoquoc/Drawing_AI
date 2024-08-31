import tkinter as tk
from tkinter import ttk
from tkinter import*
from tkinter import colorchooser
import numpy as np
import cv2

# 1.Chuyển đổi ảnh màu sang ảnh grayscale
img = cv2.imread('E:\My_projects\Git_study\Drawing_AI\Drawing_AI_code\img7.jpg', cv2.IMREAD_UNCHANGED)
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey_img)
blur = cv2.GaussianBlur(invert, (21, 21), 0)
invertedblur = cv2.bitwise_not(blur)
sketch = cv2.divide(grey_img, invertedblur, scale=400.0)

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

def is_collinear(p1, p2, p3):
    # Kiểm tra xem ba điểm có nằm trên cùng một đường thẳng hay không
    return (p3[1] - p1[1]) * (p2[0] - p1[0]) == (p2[1] - p1[1]) * (p3[0] - p1[0])

def reduce_points(coords):
    reduced_coords = [coords[0]]  # Bắt đầu với điểm đầu tiên
    for i in range(1, len(coords) - 1):
        if not is_collinear(reduced_coords[-1], coords[i], coords[i + 1]):
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

if len(gray_coords) > 0:
    reduced_coords = reduce_points(gray_coords)
    draw_points(reduced_coords)  

root.mainloop()