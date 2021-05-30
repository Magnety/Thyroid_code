import cv2
import numpy as np
print("****************")
i=1
j=1
save_root = "D:\\thyroid_jpg"

np.set_printoptions(threshold=np.inf)
root1 = r"D:\thyroid_jpg\LI_GUAN_JUN\2021_3_30_10_09_05\IMG-0001-00001.jpg"
img1 = cv2.imread(root1)
print(img1.shape)
print(img1[0,:,0])
print(img1[0,:,1])
print(img1[0,:,2])

cv2.imwrite(save_root + "/%s" % i + "_%s.jpg" % j, cv2.cvtColor(img1[0:50,:,:], cv2.COLOR_RGB2BGR))

root2 = r"D:\thyroid_jpg\11270000\1_0.jpg"
#img2 = cv2.imread(root2)
#print(img2.shape)
#print(img2[0:50,:,1])