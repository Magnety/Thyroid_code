import tkinter as tk
import SimpleITK as sitk
from tkinter import *
from tkinter import filedialog
import os
import numpy as np
from PIL import Image,ImageTk
import cv2
import threading
class UI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=None)
        self.x = self.y = 0
        self.img_np = None
        self.label_np =None
        self.img_path=None
        self.label_path = None
        self.output_img_path = None
        self.output_label_path = None
        self.default_dir = None
        self.default_output_dir = None
        self.img_name = None
        self.img_names = None
        self.img_index = 300
        self.x_scale = 0
        self.y_scale = 0
        self.x_spacing = 0
        self.y_spacing = 0
        master.title('Resize System')
        master.geometry('1500x1000')
        # 文件路径
        self.file_path = None
        # 第一张和最后一张slice位置
        self.start_slice =None
        self.end_slice = None
        self.mask = None
        self.mask_np = None
        # 打开图片按钮
        self.btn_openfile = Button(master, text='Open File', width=10, height=1, command=self.loadfile)
        self.btn_openfile.place(x=5, y=5)
        #patient name
        self.patient_name = tk.StringVar()
        self.patient_name.set("Unknow")
        self.patient1 = Label(master, text="From: ")
        self.patient1.place(x=100, y=10)
        self.patient2 = Label(master, textvariable=self.patient_name)
        self.patient2.place(x=150, y=10)
        # 初始空白图像
        self.empty_img_np = np.zeros((800, 800))
        self.empty_img = Image.fromarray(self.empty_img_np)
        self.empty_render = ImageTk.PhotoImage(self.empty_img)
        # 图片标签
        self.nii_label = Label(master, text='Whole Img')
        self.nii_label.place(x=5, y=35)
        # 原始图像框
        self.nii_img = Canvas(master,width=1400,height=980)
        #self.nii_img.create_image(0, 0, anchor=NW, image=self.empty_render)
        self.nii_img.bind("<ButtonPress-1>", self.on_button_press)
        self.nii_img.bind("<B1-Motion>", self.on_move_press)
        self.nii_img.bind("<ButtonRelease-1>", self.on_button_release)
        self.nii_img.place(x=0, y=60)
        # 分割标签
        #矩形框
        self.rect1 = None
        self.rect2 =None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        # 滚动条
        # Button(root,text = '获取位置',command = show).pack()#用command回调函数获取位置
        self.timer = threading.Timer(1, self.show)
        self.timer.start()
        # 第一张和最后一张切片确定按钮
        #测试矩形框
        self.btn_predict = Button(master,text='Seg&Class',command=self.Crop)
        self.btn_predict .place(x=1410,y=500)
        self.btn_before = Button(master, text='Before', command=self.Before)
        self.btn_before.place(x=1410, y=100)
        self.btn_next = Button(master, text='Next', command=self.Next)
        self.btn_next.place(x=1410, y=200)
        #class label



#绘制矩形框
    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y
        # create rectangle if not yet exist
        # if not self.rect:
        self.rect1 = self.nii_img.create_rectangle(self.x, self.y, 1, 1, fill="",outline='red')
        print("x:%d"%self.start_x)
        print("y:%d"%self.start_y)
    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.end_x = curX
        self.end_y = curY
        # expand rectangle as you drag the mouse
        self.nii_img.coords(self.rect1, self.start_x, self.start_y, curX, curY)
        print("curx:%d" %curX)
        print("cury:%d" %curY)
    def on_button_release(self, event):
        pass

    # 打开图像
    def loadfile(self):
        self.default_dir = r"G:\Thoyroid\ThyroidProject\Data\FinallLabeledJpg"
        self.img_dir = self.default_dir + '/image/2d/'
        self.label_dir = self.default_dir + '/label_sort/2d/'
        self.img_names = os.listdir( self.img_dir)

        self.patient_name.set(self.img_names[self.img_index])
        self.label_path = self.label_dir + self.img_names[self.img_index]
        self.img_path = self.img_dir + self.img_names[self.img_index]
        self.img_index+=1
        print(self.img_path)
        print(self.label_path)
        self.img_np = cv2.imread(self.img_path)
        self.img_np = cv2.cvtColor(self.img_np, cv2.COLOR_BGR2RGB)
        self.label_np = cv2.imread(self.label_path)
        # self.label_np = cv2.cvtColor(self.label_np, cv2.COLOR_BGR2RGB)
        self.show_img()
    def Next(self):
        self.patient_name.set(self.img_names[self.img_index])
        self.label_path = self.label_dir + self.img_names[self.img_index]
        self.img_path = self.img_dir + self.img_names[self.img_index]
        self.img_index += 1
        print(self.img_path)
        print(self.label_path)
        self.img_np = cv2.imread(self.img_path)
        self.img_np = cv2.cvtColor(self.img_np, cv2.COLOR_BGR2RGB)
        self.label_np = cv2.imread(self.label_path)
        # self.label_np = cv2.cvtColor(self.label_np, cv2.COLOR_BGR2RGB)
        self.show_img()
    def Before(self):
        self.img_index -= 1
        self.patient_name.set(self.img_names[self.img_index])
        self.label_path = self.label_dir + self.img_names[self.img_index]
        self.img_path = self.img_dir + self.img_names[self.img_index]
        print(self.img_path)
        print(self.label_path)
        self.img_np = cv2.imread(self.img_path)
        self.img_np = cv2.cvtColor(self.img_np, cv2.COLOR_BGR2RGB)
        self.label_np = cv2.imread(self.label_path)
        # self.label_np = cv2.cvtColor(self.label_np, cv2.COLOR_BGR2RGB)
        self.show_img()

    def openfile(self):
        self.default_dir = r"G:\Thoyroid\ThyroidProject\Data\FinallLabeledJpg"
        img_dir = self.default_dir+'/image/2d/'
        label_dir = self.default_dir+'/label_sort/2d/'
        self.img_path = filedialog.askopenfilename(title=u"choose file", initialdir=(os.path.expanduser(img_dir)))
        print(self.img_path.split('/')[-1].split('.')[0])
        self.patient_name.set(self.img_path.split('/')[-1])
        self.img_name = self.img_path.split('/')[-1]
        self.label_path = label_dir + self.img_path.split('/')[-1]
        self.img_path = self.img_path.replace("/", "\\\\")
        print(self.img_path)
        print(self.label_path)
        self.img_np = cv2.imread(self.img_path)
        self.img_np = cv2.cvtColor(self.img_np, cv2.COLOR_BGR2RGB)

        self.label_np = cv2.imread(self.label_path)
        #self.label_np = cv2.cvtColor(self.label_np, cv2.COLOR_BGR2RGB)
        self.show_img()
    def Crop(self):
        self.default_output_dir = "G:/Thoyroid/ThyroidProject/Data/finallcroplabeledjpg"
        self.output_img_path =self.default_output_dir+'/image/2d'
        self.output_label_path = self.default_output_dir+'/label_sort/2d'
        if not os.path.isdir(self.output_img_path):
            os.makedirs(self.output_img_path)
        if not os.path.isdir(self.output_label_path):
            os.makedirs(self.output_label_path)
        self.output_img_path = self.output_img_path+'/'+self.img_path.split('/')[-1]
        self.output_label_path = self.output_label_path+'/'+self.img_path.split('/')[-1]
        self.img_np = cv2.cvtColor(self.img_np, cv2.COLOR_RGB2BGR)
        #self.label_np = cv2.cvtColor(self.label_np, cv2.COLOR_RGB2BGR)
        print(self.img_np.shape)
        print(self.label_np.shape)
        print(self.output_img_path)
        print(self.output_label_path)
        cv2.imwrite(self.output_img_path, self.img_np[self.start_y:self.end_y,self.start_x:self.end_x,:])
        cv2.imwrite(self.output_label_path, self.label_np[self.start_y:self.end_y,self.start_x:self.end_x,:])

    # 裁剪图像
    

    # 显示图像
    def show_img(self):
        self.nii_img.delete(tk.ALL)
        img = Image.fromarray(self.img_np[ :, :])
        render = ImageTk.PhotoImage(img)
        self.nii_img.image = render
        self.nii_img.create_image(0, 0, anchor=NW, image=render)

    #


    # 滑块函数：
    def wheel(self,e):
        if e.delta > 0:
            self.scale.set(self.scale.get() + 1)
        else:
            self.scale.set(self.scale.get() - 1)

    def show(self):
        self.timer = threading.Timer(1, self.show)
        self.timer.start()




    #进行预测


if __name__ == "__main__":
    root=Tk()
    app = UI(root)
    root.mainloop()