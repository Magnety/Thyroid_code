import os
import sys
from shutil import copyfile

sort_dir = "G:\\Thoyroid\\ThyroidProject\\Data\\FinallLabeledJpg\\0530\\image"
input_dir = "G:\\Thoyroid\\ThyroidProject\\Data\\FinallLabeledJpg\\0530\\label"
output_dir = "G:\\Thoyroid\\ThyroidProject\\Data\\FinallLabeledJpg\\0530\\label_sort"
class_names = os.listdir(sort_dir)
for class_name in class_names:
    class_dir = sort_dir + '/' + class_name
    img_names = os.listdir(class_dir)
    for img_name in img_names:
        copyfile(input_dir+'/'+img_name,output_dir+'/'+class_name+'/'+img_name)