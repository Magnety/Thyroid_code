import os
import sys
from shutil import copyfile

sort_dir = "D:\\ThyroidProject\\Data\\FinallLabeledJpg\\image"
input_dir = "D:\\ThyroidProject\\Data\\FinallLabeledJpg\\label"
output_dir = "D:\\ThyroidProject\\Data\\FinallLabeledJpg\\label_sort"
class_names = os.listdir(sort_dir)
for class_name in class_names:
    class_dir = sort_dir + '/' + class_name
    img_names = os.listdir(class_dir)
    for img_name in img_names:
        copyfile(input_dir+'/'+img_name,output_dir+'/'+class_name+'/'+img_name)