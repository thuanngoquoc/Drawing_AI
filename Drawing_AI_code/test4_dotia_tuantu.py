import tkinter as tk
from tkinter import *
import numpy as np
import cv2

# 1. Chuyển đổi ảnh màu sang ảnh grayscale
img = cv2.imread('E:\My_projects\Git_study\Drawing_AI\Drawing_AI_code\img7.jpg', cv2.IMREAD_UNCHANGED)
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey_img)
blur = cv2.GaussianBlur(invert, (21, 21), 0)
invertedblur = cv2.bitwise_not(blur)
sketch = cv2.divide(grey_img, invertedblur, scale=256.0)

# 2. Điều chỉnh kích thước canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=1100, height=1100)
canvas.pack()

# 3. Tạo ngưỡng đen xám
black_threshold = 0
gray_upper_bound = 225
gray_mask = (sketch >= black_threshold) & (sketch <= gray_upper_bound)
gray_coords = np.column_stack(np.where(gray_mask))


stroke_color = tk.StringVar(value="black")
point_size = 5
delay = 1000  # Độ trễ giữa các vòng (tính bằng mili giây)
white_pixel_threshold = 240

def is_collinear(p1, p2, p3, threshold=0.00001):
    return abs((p3[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p3[0] - p1[0])) <= threshold

def reduce_points(coords, threshold=0.01):
    reduced_coords = [coords[0]]
    for i in range(1, len(coords) - 1):
        if not is_collinear(reduced_coords[-1], coords[i], coords[i + 1], threshold):
            reduced_coords.append(coords[i])
    reduced_coords.append(coords[-1])
    return reduced_coords

def draw_points(coords, index=0):
    if index < len(coords):
        point = coords[index]
        if sketch[point[0], point[1]] <= white_pixel_threshold:
            x, y = point[1], point[0]
            canvas.create_oval(x - point_size // 2, y - point_size // 2, x + point_size // 2, y + point_size // 2, fill=stroke_color.get(), outline=stroke_color.get())
        root.after(1, draw_points, coords, index + 1)

def get_outermost_points(coords, iteration, max_iteration):
    center = np.mean(coords, axis=0).astype(int)
    max_distance = np.linalg.norm(np.array([0, 0]) - center)
    current_distance_threshold = max_distance * (1 - iteration / max_iteration)
    selected_points = []

    for point in coords:
        distance = np.linalg.norm(point - center)
        if distance >= current_distance_threshold:
            selected_points.append(point)
    
    return np.array(selected_points)

def recursive_ray_casting(coords, iteration=1, max_iteration= 5):
    if iteration > max_iteration or len(coords) == 0:
        return

    outer_points = get_outermost_points(coords, iteration, max_iteration)
    reduced_coords = reduce_points(outer_points)
    
    draw_points(reduced_coords)
    
    root.after(delay, recursive_ray_casting, coords, iteration + 1, max_iteration)

# Khởi động quá trình dò tia
print(f'Tọa độ pixel đen xám: {gray_coords}') # hiển thị dưới dạng (y,x)
if len(gray_coords) > 0:
    recursive_ray_casting(gray_coords, iteration=1, max_iteration= 6)

root.mainloop()
