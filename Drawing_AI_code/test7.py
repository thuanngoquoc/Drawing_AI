import tkinter as tk
from tkinter import colorchooser
import numpy as np
import cv2

# 1. Chuyển đổi ảnh màu sang ảnh grayscale
img = cv2.imread('E:\My_projects\Git_study\Drawing_AI\Drawing_AI_code\img7.jpg', cv2.IMREAD_UNCHANGED)
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey_img)
blur = cv2.GaussianBlur(invert, (21, 21), 0)
invertedblur = cv2.bitwise_not(blur)
sketch = cv2.divide(grey_img, invertedblur, scale=400.0)

# 2. Điều chỉnh kích thước canvas
canvas_width, canvas_height = sketch.shape[1], sketch.shape[0]
root = tk.Tk()
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# 3. Cài đặt thông số dò tia
stroke_color = tk.StringVar(value="black")
point_size = 3
delay = 1
white_pixel_threshold = 240  # Ngưỡng để xác định pixel trắng
num_rays = 360  # Số lượng tia để quét

# 4. Dò tia từ biên vào trong
def ray_casting_from_edges(sketch, angle):
    coords = []
    x0, y0 = None, None
    
    if 0 <= angle < 90:  # Quét từ biên phải xuống dưới
        x0, y0 = canvas_width - 1, 0
    elif 90 <= angle < 180:  # Quét từ biên dưới sang trái
        x0, y0 = canvas_width - 1, canvas_height - 1
    elif 180 <= angle < 270:  # Quét từ biên trái lên trên
        x0, y0 = 0, canvas_height - 1
    else:  # Quét từ biên trên sang phải
        x0, y0 = 0, 0
    
    for i in range(max(sketch.shape)):
        x = int(x0 + i * np.cos(np.radians(angle)))
        y = int(y0 + i * np.sin(np.radians(angle)))
        if 0 <= x < sketch.shape[1] and 0 <= y < sketch.shape[0]:
            if sketch[y, x] <= white_pixel_threshold:
                coords.append((y, x))
        else:
            break

    return coords

# 5. Tạo danh sách các điểm từ các tia, đảo ngược thứ tự để vẽ từ ngoài vào trong
ray_points = []
for angle in np.linspace(0, 360, num_rays, endpoint=False):
    points = ray_casting_from_edges(sketch, angle)
    ray_points.extend(points[::-1])  # Đảo ngược thứ tự điểm để vẽ từ ngoài vào trong

# Kiểm tra số lượng điểm thu thập được
print(f"Số lượng điểm thu thập được: {len(ray_points)}")

def draw_points(coords, index=0):
    if index < len(coords):
        point = coords[index]
        x, y = point[1], point[0]
        canvas.create_oval(x - point_size // 2, y - point_size // 2, x + point_size // 2, y + point_size // 2, fill=stroke_color.get(), outline=stroke_color.get())
        root.after(delay, draw_points, coords, index + 1)

if len(ray_points) > 0:
    draw_points(ray_points)

root.mainloop()
