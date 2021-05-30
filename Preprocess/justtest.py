
import pydicom
import os
import cv2
from matplotlib import pyplot as plt
import numpy as np

np.set_printoptions(threshold=np.inf)

ds = pydicom.read_file("D:\\jiazhuangxian\\DICOMDIR")
save_root = "D:\\thyroid_jpg"
#print(ds)
pixel_data = list()
i=0
j=0
print("****************")
path = r"D:\jiazhuangxian\DICOM\20210331\11270000\16476408"
dcm = pydicom.dcmread(path)
print(dcm)
#print(dcm.pixel_array[0].shape)
#cv2.imwrite(save_root + "/%s" % i + "_%s.jpg" % j, cv2.cvtColor(dcm.pixel_array[0,0:50,:,:], cv2.COLOR_RGB2BGR))
print(dcm.pixel_array[0,0,:,0])
print(dcm.pixel_array[0,0,:,1])
print(dcm.pixel_array[0,0,:,2])

