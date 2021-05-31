import SimpleITK as sitk
import numpy as np
import os
import sys
import cv2
input_dir = "G:\\Thoyroid\\ThyroidProject\\Data\\FinallLabeledNii\\0530"
output_dir = "G:\\Thoyroid\\ThyroidProject\\Data\\FinallLabeledJpg\\0530"
match_txt = "G:\\Thoyroid\\ThyroidProject\\Data\\FinallLabeledJpg\\0530\\match.txt"

class_names = os.listdir(input_dir)
print(class_names)
i=1
j=56
k=0
class_name = class_names[1]
class_dir = input_dir+"/"+class_name
patient_names = os.listdir(class_dir)
j=56
for patient_name in patient_names:
    patient_img_dir = class_dir+'/'+patient_name+'/image'
    patient_label_dir = class_dir+'/'+patient_name+'/lable'
    patient_label_names = os.listdir(patient_label_dir)
    k=0
    for label_name in patient_label_names:
        print(patient_label_dir+'/'+label_name)
        label = sitk.ReadImage(patient_label_dir+'/'+label_name)
        img = sitk.ReadImage(patient_img_dir+'/'+label_name)
        img_np = sitk.GetArrayFromImage(img)
        label_np = sitk.GetArrayFromImage(label)
        print(img_np.shape)
        print(label_np.shape)
        l=0
        if img_np.ndim==3:
            #if label_np.shape[0]==1:
            img_jgp = cv2.normalize(img_np[:, :, :], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            label_jpg = cv2.normalize(label_np.transpose(1,2,0), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            img_path = output_dir+'/image'+'/{}_{}_{}_{}.jpg'.format(i,j,k,l)
            label_path = output_dir+'/label'+'/{}_{}_{}_{}.jpg'.format(i,j,k,l)
            img_jgp = cv2.cvtColor(img_jgp, cv2.COLOR_RGB2BGR)
            cv2.imwrite(img_path,img_jgp)
            cv2.imwrite(label_path,label_jpg)
            with open(match_txt, "a") as file:
                file.write(class_name+'/'+patient_name+'/'+label_name+'->>'+'{}_{}_{}_{}.jpg'.format(i,j,k,l)+'\n')
        else:
            slice_num = 0
            for num in range(label_np.shape[0]):
                if np.mean(label_np[num]):
                    slice_num+=1
            if slice_num>30:
                for num in range(label_np.shape[0]):
                    if np.mean(label_np[num]) and num%50==0:
                        img_jgp = cv2.normalize(img_np[num, :, :, :], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                        label_jpg = cv2.normalize(label_np[num, :, :], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                        img_path = output_dir + '/image' + '/{}_{}_{}_{}.jpg'.format(i, j, k, l)
                        label_path = output_dir + '/label' + '/{}_{}_{}_{}.jpg'.format(i, j, k, l)
                        img_jgp = cv2.cvtColor(img_jgp, cv2.COLOR_RGB2BGR)
                        cv2.imwrite(img_path, img_jgp)
                        cv2.imwrite(label_path, label_jpg)
                        with open(match_txt, "a") as file:
                            file.write(
                                class_name + '/' + patient_name + '/' + label_name + '->>' + '{}_{}_{}_{}.jpg'.format(i,j,k,l) + '\n')
                        l += 1
            else:
                for num in range(label_np.shape[0]) :
                    if np.mean(label_np[num]):
                        img_jgp = cv2.normalize(img_np[num, :, :, :], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                        label_jpg = cv2.normalize(label_np[num, :, :], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                        img_path = output_dir + '/image' + '/{}_{}_{}_{}.jpg'.format(i, j, k, l)
                        label_path = output_dir + '/label' + '/{}_{}_{}_{}.jpg'.format(i, j, k, l)
                        img_jgp = cv2.cvtColor(img_jgp, cv2.COLOR_RGB2BGR)
                        cv2.imwrite(img_path, img_jgp)
                        cv2.imwrite(label_path, label_jpg)
                        with open(match_txt, "a") as file:
                            file.write(
                                class_name + '_' + patient_name + '_' + label_name + '->>' + '{}_{}_{}_{}.jpg'.format(i,j,k,l) + '\n')
                        l += 1
        k+=1
    j+=1
i+=1
