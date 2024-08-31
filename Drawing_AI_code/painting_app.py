import tkinter as tk
from tkinter import*
from tkinter import colorchooser


root = Tk()
root.title("PaintApp") # tiêu đề tag
root.geometry("1100x600") # kích thước khung

stroke_size =  IntVar()
stroke_size.set(1) # khi đưa biến lên mới thêm vô

stroke_color = StringVar()
stroke_color.set("black")

#Fram1: TOOLS
frame1 = Frame(root, height=100, width=1100, bg="lightblue") #tạo và xác định frame1&2 theo thứ tự hàng và cột (để màu cho biết)
frame1.grid(row=0, column=0, sticky=NSEW) # lệnh grid là lệnh hiển thị, sticky là vị trí như
                                        #NW chuyển các frame con trên frame 1 qua trái resize 2 chiều theo kích thước của frame phần tử
                                        #NSEW chuyển các frame con trên frame 1 qua trái resize chiều dọc theo frame con, giữ nguyên chiều ngang frame1
# ToolsFrame:
toolsframe=Frame(frame1, height=100, width=100, bg="lightgreen", relief=SUNKEN, borderwidth=5) # frame phần tử của frame1: Tools
toolsframe.grid(row=0, column=0)                                #relief=SUNKEN, borderwidth=5 kiểu hiển thị phần tử trên frame

#cách 1 đổi màu line:
# pencilButton=Button(toolsframe,text="Pencil",command=lambda:stroke_color.set("black")) #command=lambda:stroke_color.set("black") set màu line theo biến stroke_color
# pencilButton.grid(row=0, column=0)

# eraserButton=Button(frame1,text="Eraser",command=lambda:stroke_color.set("white"))
# eraserButton.grid(row=0, column=1)
#cách 2:
def usePencil(): # tạo hàm chức năng đổi màu
    stroke_color.set("black")
    canvas["cursor"] = "arrow"

def useEraser():
    stroke_color.set("white")
    canvas["cursor"] = DOTBOX #cursor=DOTBOX biến trỏ chuột thành ô box nhỏ

pencilButton=Button(toolsframe,text="Pencil",command=usePencil) 
pencilButton.grid(row=0, column=0)

eraserButton=Button(toolsframe,text="Eraser",command=useEraser)
eraserButton.grid(row=0, column=1)

toolslabelButton=Button(toolsframe,text="Tools")
toolslabelButton.grid(row=0, column=2)

# SizeFrame
sizeframe=Frame(frame1, height=100, width=100, bg="yellow", relief=SUNKEN, borderwidth=5) # frame phần tử của frame1: Size line
sizeframe.grid(row=0, column=4) 

defaultButton=Button(sizeframe,text="Default",width=10 ,command=usePencil) 
defaultButton.grid(row=0, column=0)

#tạo biến giá trị stroke_size
# stroke_size =  IntVar() #đã copy đưa lên đầu 

options = [1,2,3,4,5,10]

sizelist =  OptionMenu(sizeframe, stroke_size, *options) # *options hiển thị options theo chiều dọc
sizelist.grid(row=1,column=0)

sizelabelButton=Button(sizeframe,text="Size", width=10)
sizelabelButton.grid(row=2, column=0)

# ColorBoxFrame:
colorboxFrame =  Frame(frame1, height=100, width=100, bg="orange")
colorboxFrame.grid(row=0, column=5)

def selectcolor():
    selectedcolor = colorchooser.askcolor(title="Select Color")
    #print(selectedcolor) # in thông số màu RGB () ((255, 0, 0), '#ff0000') và mình chỉ cần lấy thông số #ff0000 bằng selectedcolor[1]
    #stroke_color.set(selectedcolor[1])
    if selectedcolor[1] == None: # tạo điều kiện này vì khi mở bảng selectcolor và bấm thoát selectedcolor[1] sẽ hiểu là None và bị lỗi kể cả trước đó đã chọn màu và ok
        stroke_color.set("black")
    else:
        stroke_color.set(selectedcolor[1])

colorButton = Button(colorboxFrame, text = "SelectColor", width= 10, command=selectcolor)
colorButton.grid(row=0, column=0)

# Colorframe
# colorframe=Frame(frame1,height=100,width=100,relief=SUNKEN, borderwidth=5)
# colorframe.grid(row=0, column=6)


# Frame2: CANVAS
frame2 = Frame(root, height=200, width=1100, bg="green")
frame2.grid(row=1, column=0)

#tạo vùng để thao tác vẽ:
canvas = Canvas(frame2, height=500, width=1100,bg="white") #tạo vùng để thao tác vẽ chú ý là chỉ trên frame2
canvas.grid(row=0, column=0)                              #cursor=DOTBOX biến trỏ chuột thành ô box nhỏ
# canvas = Canvas(frame2, height=200, width=1100,bg="yellow") 
# canvas.grid(row=1, column=0)

#có các chức năng tạo line, hình oval, hình chữ nhật:
# + canvas.create_line(100,100 , 200,300) 
# + canvas.create_rectangle(300,100 , 400,300, fill="yellow")
# + canvas.create_oval(200,120, 220,140,fill="black")

# tạo biến chuỗi để set màu sắc line bắt đầu sau đó set màu cho pencil và eraser
# stroke_color = StringVar() # đã copy biến đưa lên đầu
# stroke_color.set("red")

# variables for pencil

prevPoint = [0,0] # tạo biến
currentPoint = [0,0]  

def paint(event): # thiết lập hàm theo sự kiện (hành động nhấp chuột)
    #print(event.type) # in ra event.type khi nhấp chuột hiển thị dưới dạng số nhằm để xác định số cuối để dùng lệnh IF
    global prevPoint #
    global currentPoint #

    x = event.x 
    y = event.y 
    currentPoint = [x,y] 
    #canvas.create_oval(x,y, x+10,y+10,fill="black")  #tạo điểm và kích thước điểm khi nhấp chuột

    if prevPoint !=[0,0]: #!=0
        canvas.create_line(prevPoint[0],prevPoint[1] , currentPoint[0],currentPoint[1],fill=stroke_color.get(), width=stroke_size.get(), capstyle=tk.ROUND, joinstyle=tk.ROUND) # tạo line nối các điểm lại
                                                                                      #fill=stroke_color.get() đổ đầy đổi màu line bằng biến stroke_color
                                                                                      #width=stroke_size.get() size của nét
                                                                                      #canvas.line khi chỉnh size to bị rách nét khi uốn lượn
                                                                                      #capstyle=tk.ROUND, joinstyle=tk.ROUND làm mượt nét khắc phục rách nét
     
        
        #canvas.create_polygon(prevPoint[0],prevPoint[1] , currentPoint[0],currentPoint[1],fill=stroke_color.get(), outline=stroke_color.get(), width=stroke_size.get())

    prevPoint = currentPoint                                                          

    if event.type == "5": # điều kiện nếu điểm kết thúc nhấp chuột bằng 5 thì set lại prePoint và điểm nhấp tiếp theo không bị nối với điểm cuối vừa nảy

        #canvas.create_polygon(prevPoint[0],prevPoint[1] , currentPoint[0],currentPoint[1],fill="white", outline="white", width=stroke_size.get())
        #canvas.create_oval(x,y, x+stroke_size.get(),y+stroke_size.get(),fill="black")
        prevPoint = [0,0]

canvas.bind("<B1-Motion>", paint)    #Button-1 nhấp chuột liên tục chuột trái
canvas.bind("<ButtonRelease-1>", paint) #để set giá trị cuối event.type giảm đ      i 1 (chuột trái là ButtonRelease-1) tức bằng 5 mục đích để xác định điểm kết nhấp chuột

root.resizable(False,False) # tắt chức năng phóng to full tag
root.mainloop()