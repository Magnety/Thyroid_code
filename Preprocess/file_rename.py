import pydicom
import os
import cv2
import scipy.misc
import numpy as np
import SimpleITK as sitk
import shutil

path = "G:/Thoyroid/ThyroidProject/Data/raw/oldJPG/valid"
out_path = "G:/Thoyroid/ThyroidProject/Data/preprocessed/20210529/jpg"


class_names = os.listdir(path)
for class_name in class_names:

    patient_names = os.listdir(path + "/" + class_name)
    for patient_name in patient_names:
        i=0
        img_names = os.listdir(path + "/" + class_name +'/'+patient_name)
        for img_name in img_names:
            out_dir = out_path+'/'+class_name+'/'+patient_name
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir)
            shutil.copy(path + "/" + class_name +'/'+patient_name+'/'+img_name,out_dir+'/%s.jpg'%i)
            i+=1





