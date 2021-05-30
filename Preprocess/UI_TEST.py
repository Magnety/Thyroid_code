import tkinter as tk
import SimpleITK as sitk
from tkinter import *
from tkinter import filedialog
import os
import numpy as np
from PIL import Image,ImageTk
import threading
from predict import Predict
class UI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=None)
        self.x = self.y = 0
        self.img_np = None
        self.x_scale = 0
        self.y_scale = 0
        self.x_spacing = 0
        self.y_spacing = 0
        master.title('ABUS System')
        master.geometry('1800x700')
        # 文件路径
        self.file_path = None

        # 第一张和最后一张slice位置
        self.start_slice =None
        self.end_slice = None
        self.mask = None
        self.mask_np = None
        # 打开图片按钮
        self.btn_openfile = Button(master, text='Open File', width=10, height=1, command=self.openfile)
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
        self.nii_img = Canvas(master,width=800,height=800)
        #self.nii_img.create_image(0, 0, anchor=NW, image=self.empty_render)
        self.nii_img.bind("<ButtonPress-1>", self.on_button_press)
        self.nii_img.bind("<B1-Motion>", self.on_move_press)
        self.nii_img.bind("<ButtonRelease-1>", self.on_button_release)
        self.nii_img.place(x=0, y=60)

        # 分割标签
        self.mask_label = Label(master, text='Seg Img')
        self.mask_label.place(x=905, y=35)
        # seg框
        self.nii_mask = Canvas(master,width=800,height=800)
        #self.nii_mask.create_image(0, 0, anchor=NW, image=self.empty_render)
        self.nii_mask.place(x=905, y=60)

        #矩形框
        self.rect1 = None
        self.rect2 =None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        # 滚动条
        self.scale = Scale(master, orient=tk.VERTICAL, length=360, from_=0, to=317, command=self.show_nii)
        self.scale.place(x=820, y=60)

        # 绑定鼠标滚轮
        self.scale.bind("<MouseWheel>", self.wheel)
        # Button(root,text = '获取位置',command = show).pack()#用command回调函数获取位置
        self.timer = threading.Timer(1, self.show)
        self.timer.start()

        # 第一张和最后一张切片确定按钮
        self.btn_start = Button(master, text='FROM', width=8, command=self.btn_start_slice)
        self.btn_start.place(x=815, y=430)
        self.btn_end = Button(master, text=' TO ', width=8, command=self.btn_end_slice)
        self.btn_end.place(x=815, y=470)

        #清除矩形框
        self.btn_clear_rect = Button(master,text ='Clear Label',width=8,command=self._show_nii)
        self.btn_clear_rect.place(x=815,y=510)

        #测试矩形框
        self.btn_predict = Button(master,text='Seg&Class',command=self.predict)
        self.btn_predict .place(x=810,y=610)

        #class label

        self.class_label = tk.StringVar()
        self.class_label.set("Unknow")
        self.class_label1 = Label(master, text='Malignant:')
        self.class_label1.place(x=710, y=10)
        self.class_label2 = Label(master, textvariable=self.class_label)
        self.class_label2.place(x=800, y=10)
        self.class_posibility = tk.StringVar()
        self.class_posibility.set("0.0000")
        self.class_label3 = Label(master, text='Posibility:')
        self.class_label3.place(x=890, y=10)
        self.class_label4 = Label(master, textvariable=self.class_posibility)
        self.class_label4.place(x=980, y=10)


#绘制矩形框
    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        # if not self.rect:
        self.rect1 = self.nii_img.create_rectangle(self.x, self.y, 1, 1, fill="",outline='red')
        self.rect2 = self.nii_mask.create_rectangle(self.x, self.y, 1, 1, fill="",outline='red')

        print("x:%d"%self.start_x)
        print("y:%d"%self.start_y)


    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.end_x = curX
        self.end_y = curY
        # expand rectangle as you drag the mouse
        self.nii_img.coords(self.rect1, self.start_x, self.start_y, curX, curY)
        self.nii_mask.coords(self.rect2, self.start_x, self.start_y, curX, curY)

        print("curx:%d" %curX)
        print("cury:%d" %curY)

    def on_button_release(self, event):
        pass



    # 打开图像
    def openfile(self):
        default_dir = r"D:\3dbreastseg\Dataset\breast_input\test"
        path = filedialog.askopenfilename(title=u"choose file", initialdir=(os.path.expanduser(default_dir)))
        #path = filedialog.askopenfilename(title=u"choose file")

        print(path.split('/')[-1].split('.')[0])
        self.patient_name.set(path.split('/')[-1].split('.')[0])
        path = path.replace("/", "\\\\")
        self.file_path=path
        print(self.file_path)
        img_data = sitk.ReadImage(path)
        self.x_spacing =img_data.GetSpacing()[0]
        self.y_spacing =img_data.GetSpacing()[1]
        if self.x_spacing>self.y_spacing:
            self.x_scale=1
            self.y_scale=self.x_spacing/self.y_spacing
        if self.x_spacing < self.y_spacing:
            self.y_scale =1
            self.x_scale =  self.y_spacing / self.x_spacing
        if self.x_spacing == self.y_spacing:
            self.x_scale = 1
            self.y_scale = 1
        print(self.x_spacing)
        print(self.y_spacing)
        print(self.x_scale)
        print(self.y_scale)
        self.img_np = sitk.GetArrayFromImage(img_data)
        print(self.img_np.shape)
        print(self.empty_img_np.shape)
        self.mask = np.zeros_like(self.img_np)
        self.show_nii(self.scale.get())


    # 裁剪图像
    def img_np_resize(self,img_np):
        return img_np[:, 0:590, 0:690]

    # 显示图像
    def show_nii(self,val):
        slice = int(val)
        self.nii_img.delete(tk.ALL)
        self.nii_mask.delete(tk.ALL)

        self.mask_np = self.mask
        img = Image.fromarray(self.img_np[slice, :, :])
        img = img.resize((int(self.img_np.shape[2] / self.x_scale), int(self.img_np.shape[1] / self.y_scale)),Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)
        self.nii_img.image = render
        self.nii_img.create_image(0, 0, anchor=NW, image=render)
        mask_img = Image.fromarray(self.img_np[slice,:,:])
        mask_img = mask_img.convert("RGBA")
        mask_rgb = np.zeros((self.img_np.shape[1],self.img_np.shape[2],3), 'uint8')
        mask_rgb[:,:,0] = self.mask_np[slice,:,:]
        mask_tmp = Image.fromarray(mask_rgb)
        print(mask_tmp)
        mask_tmp = mask_tmp.convert("RGBA")
        mask_img = Image.blend(mask_img, mask_tmp, 0.3)
        mask_img = mask_img.resize((int(self.img_np.shape[2]/self.x_scale), int(self.img_np.shape[1] /self.y_scale)), Image.ANTIALIAS)
        mask_render = ImageTk.PhotoImage(mask_img)
        self.nii_mask.image= mask_render
        self.nii_mask.create_image(0,0,anchor=NW,image= mask_render)
    #
    def _show_nii(self):
        slice = int(self.scale.get())
        self.nii_img.delete(tk.ALL)
        self.nii_mask.delete(tk.ALL)

        self.mask_np = self.mask
        img = Image.fromarray(self.img_np[slice, :, :])
        img = img.resize((int(self.img_np.shape[2] / self.x_scale), int(self.img_np.shape[1] / self.y_scale)),
                         Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img)
        self.nii_img.image = render
        self.nii_img.create_image(0, 0, anchor=NW, image=render)
        mask_img = Image.fromarray(self.img_np[slice, :, :])
        mask_img = mask_img.convert("RGBA")
        mask_rgb = np.zeros((self.img_np.shape[1], self.img_np.shape[2], 3), 'uint8')
        mask_rgb[:, :, 0] = self.mask_np[slice, :, :]
        mask_tmp = Image.fromarray(mask_rgb)
        print(mask_tmp)
        mask_tmp = mask_tmp.convert("RGBA")
        mask_img = Image.blend(mask_img, mask_tmp, 0.3)
        mask_img = mask_img.resize((int(self.img_np.shape[2] / self.x_scale), int(self.img_np.shape[1] / self.y_scale)),
                                   Image.ANTIALIAS)
        mask_render = ImageTk.PhotoImage(mask_img)
        self.nii_mask.image = mask_render
        self.nii_mask.create_image(0, 0, anchor=NW, image=mask_render)

    # 滑块函数：
    def wheel(self,e):
        if e.delta > 0:
            self.scale.set(self.scale.get() + 1)
        else:
            self.scale.set(self.scale.get() - 1)

    def show(self):
        self.timer = threading.Timer(1, self.show)
        self.timer.start()

    # 确定第一张和最后一张函数
    def btn_start_slice(self):
        self.start_slice=int(self.scale.get())
        print("start:%d" % self.start_slice)

    def btn_end_slice(self):
        self.end_slice = int(self.scale.get())
        print("end:%d" % self.end_slice)


    #进行预测
    def predict(self):
        path = self.file_path
        img_data = sitk.ReadImage(path)
        img= sitk.GetArrayFromImage(img_data)
        print(int(self.start_y*self.x_scale))
        print(int(self.end_y*self.x_scale))
        print(int(self.start_x*self.y_scale))
        print(int(self.end_x*self.y_scale))
        predict0,seg0,cls0,posibility0 = Predict(img[self.start_slice:self.end_slice,int(self.start_y*self.y_scale):int(self.end_y*self.y_scale),int(self.start_x*self.x_scale):int(self.end_x*self.x_scale)],0)
        predict1,seg1,cls1,posibility1 = Predict(img[self.start_slice:self.end_slice,int(self.start_y*self.y_scale):int(self.end_y*self.y_scale),int(self.start_x*self.x_scale):int(self.end_x*self.x_scale)],1)
        predict2,seg2,cls2,posibility2 = Predict(img[self.start_slice:self.end_slice,int(self.start_y*self.y_scale):int(self.end_y*self.y_scale),int(self.start_x*self.x_scale):int(self.end_x*self.x_scale)],2)
        posibility = (posibility0+posibility1+posibility2)/3
        #posibility = (posibility1)
        if posibility>=0.5:
            cls =1
        else :
            cls =0
        seg = np.zeros_like(predict1)
        predict = (predict0)
        #predict = (predict0)/1

        seg[predict>0.35]=1
        slice = int(self.scale.get())
        self.mask[:,:,:]= 0
        self.mask[self.start_slice:self.end_slice,int(self.start_y*self.y_scale):int(self.end_y*self.y_scale),int(self.start_x*self.x_scale):int(self.end_x*self.x_scale)]=seg
        #self.mask[self.start_slice:self.end_slice,int(self.start_y*self.y_scale):int(self.end_y*self.y_scale),int(self.start_x*self.x_scale):int(self.end_x*self.x_scale)]=img[self.start_slice:self.end_slice, int(self.start_y * self.y_scale):int(self.end_y * self.y_scale),int(self.start_x * self.x_scale):int(self.end_x * self.x_scale)]
        mask_img = sitk.GetImageFromArray(self.mask)
        mask_img = sitk.BinaryFillhole(mask_img)
        self.mask = sitk.GetArrayFromImage(mask_img)
        self.mask[self.mask==1]=255
        self.show_nii(slice)
        print("class：%d"%cls)
        print(seg.shape)
        if(cls==1):
            self.class_label.set("True")
        else:
            self.class_label.set("False")
        self.class_posibility.set(posibility)


if __name__ == "__main__":
    root=Tk()
    app = UI(root)
    root.mainloop()