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
gray_upper_bound = 225  # giá trị trên ngưỡng xám
# Điều kiện chọn pixel theo ngưỡng
gray_mask = (sketch >= black_threshold) & (sketch <= gray_upper_bound)
gray_coords = np.column_stack(np.where(gray_mask)) 


stroke_color = tk.StringVar(value="black") 
point_size = 5
delay = 1 
points_per_iteration = 1
white_pixel_threshold = 240  # Ngưỡng để xác định pixel trắng

# 3. Xác định tâm của hình ảnh
height, width = sketch.shape
center_x, center_y = width // 2, height // 2

# 4. Chia hình ảnh thành các ô (grid cells)
cell_size = 2  # Kích thước mỗi ô (pixel)
grid_coords = {}

for y in range(0, height, cell_size):
    for x in range(0, width, cell_size):
        cell_pixels = []
        for j in range(y, min(y + cell_size, height)):
            for i in range(x, min(x + cell_size, width)):
                if sketch[j, i] <= white_pixel_threshold:
                    cell_pixels.append((j, i))
        if cell_pixels:
            # Tính trung bình tọa độ của các pixel trong ô
            avg_y = int(np.mean([p[0] for p in cell_pixels]))
            avg_x = int(np.mean([p[1] for p in cell_pixels]))
            distance = np.sqrt((avg_x - center_x) ** 2 + (avg_y - center_y) ** 2)
            grid_coords[(avg_y, avg_x)] = distance

# 5. Sắp xếp các tọa độ theo khoảng cách từ xa nhất đến gần nhất
sorted_coords = sorted(grid_coords.items(), key=lambda x: x[1], reverse=True)


pen_id = None

def draw_points(coords, index=0):
    global pen_id
    if index < len(coords):
        for _ in range(points_per_iteration):
            if index >= len(coords):
                break
            (y, x), _ = coords[index]
            canvas.create_oval(
                x - point_size // 2, y - point_size // 2,
                x + point_size // 2, y + point_size // 2,
                fill=stroke_color.get(), outline=stroke_color.get()
            )
            index += 1
        root.after(delay, draw_points, coords, index)

if len(sorted_coords) > 0:
    draw_points(sorted_coords)

# Start the Tkinter main loop
root.mainloop()