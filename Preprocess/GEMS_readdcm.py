import pydicom
import os
import cv2
import scipy.misc
import numpy as np
import SimpleITK as sitk
from PIL import Image
from matplotlib import pyplot as plt

path = "G:\\Thoyroid\\ThyroidProject\\Data\\raw\\0416\\GEMS_IMG"
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
                        dcm = pydicom.dcmread(series_file_name)
                        print(series_file_name)
                        print("name:", dcm.PatientID)

