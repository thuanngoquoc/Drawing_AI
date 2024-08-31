import tkinter as tk
import numpy as np
import cv2
import math

# 1. Chuyển đổi ảnh màu sang ảnh grayscale
img = cv2.imread('E:\My_projects\Git_study\Drawing_AI\Drawing_AI_code\img7.jpg', cv2.IMREAD_UNCHANGED)
if img is None:
    print("Error: File not found or cannot be opened.")
    exit()

grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey_img)
blur = cv2.GaussianBlur(invert, (21, 21), 0)
invertedblur = cv2.bitwise_not(blur)
sketch = cv2.divide(grey_img, invertedblur, scale=400.0)

# 2. Điều chỉnh kích thước canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=1100, height=1100, bg='white')
canvas.pack()

# 3. Tạo ngưỡng đen xám
black_threshold = 0  # giá trị ngưỡng đen
gray_upper_bound = 225 # giá trị trên ngưỡng xám
gray_mask = (sketch >= black_threshold) & (sketch <= gray_upper_bound)
gray_coords = np.column_stack(np.where(gray_mask))

# 4. Tính khoảng cách từ các điểm đến trung tâm
center_x, center_y = grey_img.shape[1] // 2, grey_img.shape[0] // 2
distances = [math.sqrt((x - center_x)**2 + (y - center_y)**2) for y, x in gray_coords]

# 5. Sắp xếp các điểm theo khoảng cách từ ngoài vào trong
sorted_indices = np.argsort(distances)
sorted_coords = gray_coords[sorted_indices]

stroke_color = tk.StringVar(value="black")  # Màu điểm vẽ
point_size = 3  # Kích thước điểm
delay = 1 # Độ trễ giữa các điểm, tính bằng mili giây
white_pixel_threshold = 240  # Ngưỡng để xác định pixel trắng

def draw_points(coords, index=0):
    if index < len(coords):
        point = coords[index]
       
        if sketch[point[0], point[1]] <= white_pixel_threshold:
            x, y = point[1], point[0]  
            canvas.create_oval(x - point_size // 2, y - point_size // 2, x + point_size // 2, y + point_size // 2, fill=stroke_color.get(), outline=stroke_color.get())
        root.after(delay, draw_points, coords, index + 1)

if len(sorted_coords) > 0:
    draw_points(sorted_coords)  

root.mainloop()
