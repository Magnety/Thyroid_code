import pydicom
import os
import cv2
import scipy.misc
import numpy as np
import SimpleITK as sitk
from PIL import Image
from matplotlib import pyplot as plt
ds = pydicom.read_file("D:\\jiazhuangxian\\0416\\DICOMDIR")
save_root = "D:\\thyroid_jpg"
print(ds)
#print(ds.RescaleIntercept)
pixel_data = list()
i=0
for record in ds.DirectoryRecordSequence:
    print("iter:",i)
    if record.DirectoryRecordType == "IMAGE":
        # Extract the relative path to the DICOM file
        path = os.path.join("D:\\jiazhuangxian\\0416\\",*record.ReferencedFileID)
        save_path1 = os.path.join("D:\\thyroid_jpg\\jpg\\",record.ReferencedFileID[1],record.ReferencedFileID[2])
        save_path = os.path.join("D:\\thyroid_jpg\\", record.ReferencedFileID[1],record.ReferencedFileID[2])
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        if not os.path.isdir(save_path1):
            os.makedirs(save_path1)
        print(path)
        print(*record.ReferencedFileID)
        dcm = pydicom.dcmread(path)
        #print(dcm.RescaleIntercept)
        print(dcm.pixel_array.shape)
        # Now get your image data
        if dcm.pixel_array.ndim==3:
            #im = Image.fromarray(dcm.pixel_array)
            #cv2.imwrite(save_path1+"/%s.jpg"%i,cv2.cvtColor(dcm.pixel_array, cv2.COLOR_RGB2BGR))
            #im.save(save_path+"/%s.jpg"%i)
            #shape1,shape2,shape3 = dcm.pixel_array.shape[0],dcm.pixel_array.shape[1],dcm.pixel_array.shape[2]
            #serial_img = np.zeros((1,shape1,shape2,shape3))
            #serial_img[0] = dcm.pixel_array
            print(dcm.pixel_array.shape)
            #img = sitk.GetImageFromArray(serial_img)
            #sitk.WriteImage(img,save_path+"/%s.nii.gz"%record.ReferencedFileID[3])
            i+=1
        else:
            print("x")
            #serial_img = np.zeros_like(dcm.pixel_array)
           # for j in range(dcm.pixel_array.shape[0]):
                # imcopy[:, :, 0] = cv2.normalize(dcm.pixel_array[j,:,:,0], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                # imcopy[:, :, 1] = cv2.normalize(dcm.pixel_array[j,:,:,1], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                # imcopy[:, :, 2] = cv2.normalize(dcm.pixel_array[j,:,:,2], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                # im = Image.fromarray(dcm.pixel_array[j])
                #print("save 2")
                # im.save(save_path+ "/%s"%i+"_%s.jpg" %j)\
                # save_pic = cv2.normalize(dcm.pixel_array[j], None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                #cv2.imwrite(save_path1 + "/%s" % i + "_%s.jpg" % j,
                            #cv2.cvtColor(dcm.pixel_array[j], cv2.COLOR_YCrCb2RGB))
               # serial_img[j, :, :, :] = cv2.cvtColor(dcm.pixel_array[j], cv2.COLOR_YCrCb2BGR)
           # if j > 800:
                #img = sitk.GetImageFromArray(serial_img[0:800,:,:,:])
           # else:
               # img = sitk.GetImageFromArray(serial_img)
            # np.transpose(img, [2,1,0])
            #sitk.WriteImage(img, save_path + "/%s.nii.gz" %record.ReferencedFileID[3])
            #i += 1
