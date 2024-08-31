import cv2
import numpy as np
img = cv2.imread('E:\My_projects\Git_study\Drawing_AI\Drawing_AI_code\img7.jpg', cv2.IMREAD_UNCHANGED)
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
invert = cv2.bitwise_not(grey_img)
blur = cv2.GaussianBlur(invert, (21, 21), 0)
invertedblur = cv2.bitwise_not(blur)

# ảnh thang độ xám ban đầu grey_img được chia cho 
# được chia cho ảnh đảo ngược làm mờ invertedblur 
# với một hệ số tỷ lệ (scale) là 270.0 để tăng cường độ tương phản. Kết quả là một bản phác thảo được lưu vào biến sketch.
sketch = cv2.divide(grey_img, invertedblur, scale=270.0)

# Màu đen xám: giá trị gần trung bình của các giá trị đen xám
black_threshold = 0  # giá trị ngưỡng đen
gray_upper_bound = 225  # giá trị trên ngưỡng xám

# Tìm các pixel đen xám
gray_mask = (sketch >= black_threshold) & (sketch <= gray_upper_bound)
gray_coords = np.column_stack(np.where(gray_mask)) #Sử dụng np.where() để xác định tọa độ của các pixel thỏa mãn điều kiện.

# In kết quả
print(f'Tọa độ pixel đen xám: {gray_coords}') # hiển thị dưới dạng (y,x)

# Hiển thị ảnh với các pixel đen và xám được đánh dấu
output_img = img.copy()
output_img[gray_mask] = [255, 0, 0]   # đánh dấu pixel xám bằng màu xanh

# Hiển thị ảnh
cv2.imshow('sketch',sketch)
cv2.imshow('output_img',output_img) 
cv2.waitKey(0)
cv2.destroyAllWindows()