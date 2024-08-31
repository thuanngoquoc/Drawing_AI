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
# ảnh thang độ xám ban đầu grey_img được chia cho 
# được chia cho ảnh đảo ngược làm mờ invertedblur 
# với một hệ số tỷ lệ (scale) là 270.0 để tăng cường độ tương phản. Kết quả là một bản phác thảo được lưu vào biến sketch.
sketch = cv2.divide(grey_img, invertedblur, scale=400.0)

#2.Điều chỉnh kích thước canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=1100, height=1100)
canvas.pack()
#PAPER_SIZES = {
#    'A4': (210 * 96 / 25.4, 297 * 96 / 25.4),  # chiều rộng, chiều cao
#    'A3': (297 * 96 / 25.4, 420 * 96 / 25.4),  # chiều rộng, chiều cao
#}
#ORIENTATIONS = ['Portrait', 'Landscape']
#
#def create_canvas(size, orientation):
#    width, height = size
#    if orientation == 'Landscape':
#        width, height = height, width
#    canvas.config(width=width, height=height)
#    canvas.pack()
#
#def apply_settings():
#    size = PAPER_SIZES[size_var.get()]
#    orientation = orientation_var.get()
#    create_canvas(size, orientation)
#
#root = tk.Tk()
#root.title("Canvas Size Selector")
#
## Tạo các widget để chọn kích thước và hướng
#size_var = tk.StringVar(value='A4')
#orientation_var = tk.StringVar(value='Portrait')
#
#tk.Label(root, text="Select Paper Size:").pack()
#size_menu = ttk.Combobox(root, textvariable=size_var, values=list(PAPER_SIZES.keys()))
#size_menu.pack()
#
#tk.Label(root, text="Select Orientation:").pack()
#orientation_menu = ttk.Combobox(root, textvariable=orientation_var, values=ORIENTATIONS)
#orientation_menu.pack()
#
#apply_button = tk.Button(root, text="Apply", command=apply_settings)
#apply_button.pack()
## Tạo canvas ban đầu
#canvas = tk.Canvas(root)
#canvas.pack()
#
# 3.Tạo ngưỡng đen xám
black_threshold = 0  # giá trị ngưỡng đen
gray_upper_bound = 225 # giá trị trên ngưỡng xám
# Điều kiện chọn pixel theo ngưỡng
gray_mask = (sketch >= black_threshold) & (sketch <= gray_upper_bound)
gray_coords = np.column_stack(np.where(gray_mask)) # Sử dụng np.where() để xác định tọa độ của các pixel thỏa mãn điều kiện.
# In kết quả
#print(f'Tọa độ pixel đen xám: {gray_coords}') # hiển thị dưới dạng (y,x)

#stroke_color = tk.StringVar(value="black")  # Màu nét vẽ
#stroke_size = tk.IntVar(value=1)  # Độ dày nét vẽ
#delay = 1  # Độ trễ giữa các nét vẽ, tính bằng mili giây
#
#def draw_lines_with_delay(coords, index=1, prev_point=None):
#    if index < len(coords):
#        current_point = coords[index]
#        if prev_point is not None:
#            canvas.create_line(prev_point[1], prev_point[0], current_point[1], current_point[0], fill=stroke_color.get(), width=stroke_size.get(), capstyle=tk.ROUND, joinstyle=tk.ROUND)
#        root.after(delay, draw_lines_with_delay, coords, index + 1, current_point)
#
#if len(gray_coords) > 0:
#    prev_point = gray_coords[0]  # Điểm đầu tiên
#    draw_lines_with_delay(gray_coords, 1, prev_point)  # Bắt đầu vẽ từ điểm thứ 2

# 4.Vẽ điểm hình oval theo tọa độ pixel

##Fram1: TOOLS
#frame1 = Frame(root, height=100, width=1100, bg="lightblue") #tạo và xác định frame1&2 theo thứ tự hàng và cột (để màu cho biết)
#frame1.grid(row=0, column=0, sticky=NSEW) 
## SizeFrame
#sizeframe=Frame(frame1, height=100, width=100, bg="yellow", relief=SUNKEN, borderwidth=5) # frame phần tử của frame1: Size line
#sizeframe.grid(row=0, column=4) 
#
#stroke_size = tk.IntVar()
#stroke_size.set(1) # khi đưa biến lên mới thêm vô
#
#stroke_color = tk.StringVar()
#stroke_color.set("black")
#
#options = [1,2,3,4,5,10]
#
#sizelist =  OptionMenu(sizeframe, stroke_size, *options) # *options hiển thị options theo chiều dọc
#sizelist.grid(row=1,column=0)
#
#sizelabelButton=Button(sizeframe,text="Size", width=10)
#sizelabelButton.grid(row=2, column=0)
#
## ColorBoxFrame:
#colorboxFrame =  Frame(frame1, height=100, width=100, bg="orange")
#colorboxFrame.grid(row=0, column=5)
#
#def selectcolor():
#    selectedcolor = colorchooser.askcolor(title="Select Color")
#    #print(selectedcolor) # in thông số màu RGB () ((255, 0, 0), '#ff0000') và mình chỉ cần lấy thông số #ff0000 bằng selectedcolor[1]
#    #stroke_color.set(selectedcolor[1])
#    if selectedcolor[1] == None: # tạo điều kiện này vì khi mở bảng selectcolor và bấm thoát selectedcolor[1] sẽ hiểu là None và bị lỗi kể cả trước đó đã chọn màu và ok
#        stroke_color.set("black")
#    else:
#        stroke_color.set(selectedcolor[1])
#
#colorButton = Button(colorboxFrame, text = "SelectColor", width= 10, command=selectcolor)
#colorButton.grid(row=0, column=0)
#
#
stroke_color = tk.StringVar(value="black")  # Màu điểm vẽ
point_size = 3  # Kích thước điểm
delay = 1 # Độ trễ giữa các điểm, tính bằng mili giây
white_pixel_threshold = 240  # Ngưỡng để xác định pixel trắng

def draw_points(coords, index=0):
    if index < len(coords):
        point = coords[index]
        # Chỉ vẽ điểm nếu pixel hiện tại không phải là pixel trắng
        if sketch[point[0], point[1]] <= white_pixel_threshold:
            x, y = point[1], point[0]  # Chuyển đổi tọa độ từ (y, x) thành (x, y)
            canvas.create_oval(x -point_size // 2, y - point_size // 2, x + point_size // 2, y + point_size // 2, fill=stroke_color.get(), outline=stroke_color.get())
        root.after(delay, draw_points, coords, index + 1)

if len(gray_coords) > 0:
    draw_points(gray_coords)  # Bắt đầu vẽ từ điểm đầu tiên

root.mainloop()