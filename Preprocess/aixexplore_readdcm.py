import pydicom
import os
import cv2
import scipy.misc
import numpy as np
import SimpleITK as sitk
from PIL import Image
from matplotlib import pyplot as plt

path = "D:\\ThyroidProject\\Data\\raw\\0416\\Aixplorer_Series"
names = os.listdir(path)
for name in names:
    print(name)
    ds = pydicom.read_file("D:\\ThyroidProject\\Data\\raw\\0416\\Aixplorer_Series\\%s\\DICOMDIR"%name)
    print(ds)
    print("///////////////////////////////////////////////////////////////////////////////")

