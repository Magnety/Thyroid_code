import pydicom
import os
import cv2
import scipy.misc
import numpy as np
import SimpleITK as sitk
from PIL import Image
from matplotlib import pyplot as plt
ds = pydicom.read_file("D:\\jiazhuangxian\\0413\\DICOMDIR")
save_root = "D:\\thyroid_jpg"
#print(ds.PatientName)
#print(ds.RescaleIntercept)
pixel_data = list()
i=0
for record in ds.DirectoryRecordSequence:
    if record.DirectoryRecordType == "IMAGE":
        path = os.path.join("D:\\jiazhuangxian\\0413\\", *record.ReferencedFileID)
        print("id:", *record.ReferencedFileID)
        dcm = pydicom.dcmread(path)
        print("name:",dcm.PatientName)
        #print(dcm)
