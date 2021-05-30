
import pydicom
import os
import cv2
import scipy.misc
import numpy as np
import SimpleITK as sitk
from PIL import Image
from matplotlib import pyplot as plt
path = "D:\\ThyroidProject\\Data\\raw\\0416\\GEMS_IMG"
names1 = os.listdir(path)
for name1 in names1:
    names2 = os.listdir(path+"\\"+name1)
    for name2 in names2:
        names3 = os.listdir(path+"\\"+name1+"\\"+name2)
        for name3 in names3:
            print(name3)
            dir_path = path+"\\"+name1+"\\"+name2+"\\"+name3
            reader = sitk.ImageSeriesReader()
            series_IDs = reader.GetGDCMSeriesIDs(dir_path)
            file_reader = sitk.ImageFileReader()
            i = 0
            if series_IDs:
                for series in series_IDs:
                    print(series)
                    print(series_IDs)
                    series_file_names = reader.GetGDCMSeriesFileNames(dir_path, series)
                    for series_file_name in series_file_names:
                        print(series_file_names)
                        print(series_file_name)
                        s_name = series_file_name.split('/')[-1]
                        file_reader.SetFileName(series_file_name)
                        dicom_itk = sitk.ReadImage(series_file_name)
                        dicom_np = sitk.GetArrayFromImage(dicom_itk)
                        print(dicom_np.shape)
                        save_path1 = os.path.join("D:\\ThyroidProject\\Data\\temp\\0416\\jpg\\" ,name1+"\\"+name2+"\\"+name3+"\\")
                        save_path = os.path.join("D:\\ThyroidProject\\Data\\temp\\0416\\",name1+"\\"+name2+"\\"+name3+"\\")
                        if not os.path.isdir(save_path):
                            os.makedirs(save_path)
                        if not os.path.isdir(save_path1):
                            os.makedirs(save_path1)
                        # print(path)
                        serial_img = np.zeros_like(dicom_np)
                        for j in range(dicom_np.shape[0]):
                            # imcopy[:, :, 0] = cv2.normalize(dcm.pixel_array[j,:,:,0], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                            # imcopy[:, :, 1] = cv2.normalize(dcm.pixel_array[j,:,:,1], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                            # imcopy[:, :, 2] = cv2.normalize(dcm.pixel_array[j,:,:,2], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                            # im = Image.fromarray(dcm.pixel_array[j])
                            # print("save 2")
                            # im.save(save_path+ "/%s"%i+"_%s.jpg" %j)\
                            # save_pic = cv2.normalize(dcm.pixel_array[j], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                            cv2.imwrite(save_path1 + "/%s" % i + "_%s.jpg" % j,
                                        cv2.cvtColor(dicom_np[j], cv2.COLOR_YCrCb2RGB))
                            # serial_img[j, :, :, :] = cv2.cvtColor(dicom_np[j], cv2.COLOR_YCrCb2BGR)
                            serial_img[j, :, :, :] = dicom_np[j]
                        if j > 800:
                            for _j in range(j // 800):
                                img = sitk.GetImageFromArray(serial_img[800 * _j:800 * (_j + 1), :, :, :])
                                sitk.WriteImage(img, save_path + "%s_" % s_name + "%s.nii.gz" % _j)
                            img = sitk.GetImageFromArray(serial_img[800 * (_j + 1):j, :, :, :])
                            sitk.WriteImage(img, save_path + "%s" % s_name + "_%s.nii.gz" % (_j + 1))
                        else:
                            img = sitk.GetImageFromArray(serial_img)
                            sitk.WriteImage(img, save_path + "%s.nii.gz" % s_name)
                            i += 1
                        # np.transpose(img, [2,1,0])














