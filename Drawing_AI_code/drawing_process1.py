import tkinter as tk
from tkinter import ttk
import numpy as np
import cv2
from PIL import Image, ImageTk

# 1. Chuyển đổi ảnh màu sang ảnh grayscale
img_path = 'E:\My_projects\Git_study\Drawing_AI\Drawing_AI_code\img7.jpg'
img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

if img is None:
    raise FileNotFoundError(f"Image not found at {img_path}")

grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey_img)
blur = cv2.GaussianBlur(invert, (21, 21), 0)
invertedblur = cv2.bitwise_not(blur)
sketch = cv2.divide(grey_img, invertedblur, scale=256.0)

# 2. Điều chỉnh kích thước canvas
PAPER_SIZES = {
    'A4': (210 * 96 / 25.4, 297 * 96 / 25.4),
    'A3': (297 * 96 / 25.4, 420 * 96 / 25.4),
}
ORIENTATIONS = ['Portrait', 'Landscape']

def create_canvas(size, orientation):
    width, height = size
    if orientation == 'Landscape':
        width, height = height, width
    canvas.config(width=int(width), height=int(height))
    canvas.pack()

def apply_settings():
    size = PAPER_SIZES[size_var.get()]
    orientation = orientation_var.get()
    create_canvas(size, orientation)

root = tk.Tk()
root.title("Canvas Size Selector")

# Tạo các widget để chọn kích thước và hướng
size_var = tk.StringVar(value='A4')
orientation_var = tk.StringVar(value='Portrait')

tk.Label(root, text="Select Paper Size:").pack()
size_menu = ttk.Combobox(root, textvariable=size_var, values=list(PAPER_SIZES.keys()))
size_menu.pack()

tk.Label(root, text="Select Orientation:").pack()
orientation_menu = ttk.Combobox(root, textvariable=orientation_var, values=ORIENTATIONS)
orientation_menu.pack()

apply_button = tk.Button(root, text="Apply", command=apply_settings)
apply_button.pack()

# Tạo canvas ban đầu
canvas = tk.Canvas(root)
canvas.pack()

# 3. Xác định tâm của hình ảnh
height, width = sketch.shape
center_x, center_y = width // 2, height // 2

# 4. Tạo đường xoắn ốc từ ngoài vào trong theo chiều kim đồng hồ
def generate_spiral_coords(center_x, center_y, max_radius):
    coords = []
    angle_step = 0.1
    for radius in range(0, max_radius, 1):
        angle = 0
        while angle < 2 * np.pi:
            x = int(center_x + radius * np.cos(angle))
            y = int(center_y + radius * np.sin(angle))
            if 0 <= x < width and 0 <= y < height:
                coords.append((y, x))  # y, x để phù hợp với hệ tọa độ ảnh
            angle += angle_step
    return coords

max_radius = min(center_x, center_y)
spiral_coords = generate_spiral_coords(center_x, center_y, max_radius)

pen_img = Image.open("pencil.png")  # Path to your pen image
pen_img = pen_img.resize((40, 40), Image.LANCZOS)
pen_tk = ImageTk.PhotoImage(pen_img)
# 5. Vẽ theo vòng xoắn ốc
stroke_color = tk.StringVar(value="black")
point_size = 1
delay = 1  # Reduced delay for faster drawing
points_per_iteration = 1  # Number of points to draw per iteration
white_pixel_threshold = 240

pen_tip_offset_x = -5  # Adjust based on the actual tip position in your pen image
pen_tip_offset_y = 10
pen_id = None

def draw_points(coords, index=0):
    global pen_id
    if index < len(coords):
        for _ in range(points_per_iteration):
            if index >= len(coords):
                break
            point = coords[index]
            if sketch[point[0], point[1]] <= white_pixel_threshold:
                x, y = point[1], point[0]

                if pen_id is not None:
                    canvas.delete(pen_id)

                pen_id = canvas.create_image(
                    x - pen_tip_offset_x, y - pen_tip_offset_y,
                    image=pen_tk, anchor=tk.CENTER
                )
                canvas.create_oval(
                    x - point_size // 2, y - point_size // 2,
                    x + point_size // 2, y + point_size // 2,
                    fill=stroke_color.get(), outline=stroke_color.get()
                )
            index += 1
        root.after(delay, draw_points, coords, index)
    else:
        if pen_id is not None:
            canvas.delete(pen_id)

if len(spiral_coords) > 0:
    draw_points(spiral_coords)

# Start the Tkinter main loop
root.mainloop()