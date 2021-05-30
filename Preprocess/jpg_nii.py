import pydicom
import os
import cv2
import scipy.misc
import numpy as np
import SimpleITK as sitk
from PIL import Image
from matplotlib import pyplot as plt


import pydicom
import os
import cv2
import scipy.misc
import numpy as np
import SimpleITK as sitk
import shutil

path = "G:/Thoyroid/ThyroidProject/Data/preprocessed/20210529/jpg"
out_path = "G:/Thoyroid/ThyroidProject/Data/preprocessed/20210529/nii"


class_names = os.listdir(path)
for class_name in class_names:
    patient_names = os.listdir(path + "/" + class_name)
    for patient_name in patient_names:
        img_names = os.listdir(path + "/" + class_name +'/'+patient_name)
        for img_name in img_names:
            out_dir = out_path+'/'+class_name+'/'+patient_name
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir)
            print(out_path+'/'+class_name+'/'+patient_name+'/'+img_name)
            img = cv2.imread(path+'/'+class_name+'/'+patient_name+'/'+img_name)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            shape1, shape2, shape3 = img.shape[0], img.shape[1], img.shape[2]
            serial_img = np.zeros((1, shape1, shape2, shape3))
            serial_img[0] = img
            img_out = sitk.GetImageFromArray(serial_img)
            sitk.WriteImage(img_out, out_dir + '/' + img_name.split('.')[0] + '.nii.gz')

























