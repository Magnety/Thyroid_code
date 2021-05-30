import numpy as np
import SimpleITK as sitk
import pydicom
#import h5py
import os
import nibabel as nib
import dicom2nifti


def dicom2Nii(folderPath, savefolder):
    '''
    dicom序列转成3维的nii文件，并保留原始的dicom元数据信息
    '''
    count_study = 0
    for every_study in os.listdir(folderPath):  # 遍历所有的病历号
        print("every study:",every_study)
        count_study += 1
        tmp_MR_path = os.path.join(folderPath, every_study)  # DWI ,T2等
        print("tmp_MR_path:",tmp_MR_path)
        _save_path = os.path.join(savefolder, every_study, 'Nii')
        for every_MRI in os.listdir(tmp_MR_path):  # 每个病历号下面可能有多次MRI
            print("every_MRI:",every_MRI)

            tmp_MRI_path = os.path.join(tmp_MR_path, every_MRI)
            print("tmp_MRI_path:",tmp_MRI_path)


            tmp_save_path = os.path.join(_save_path, every_MRI)
            print(" tmp_save_path:", tmp_save_path)

            if not os.path.exists(tmp_save_path):
                os.makedirs(tmp_save_path)
            all_Series_path = os.listdir(tmp_MRI_path)
            print("all_Series_path:", all_Series_path)

            # print(all_Series_path) #['DCE00001', 'DCE00002', 'DCE00003', 'DCE00004', 'DCE00005', 'DCE00006']
            for every_DCE_series in all_Series_path:
                # print(every_DCE_series) # DCE00001
                all_dicoms = os.path.join(tmp_MRI_path, every_DCE_series)
                print(all_dicoms)
                # print(all_dicoms)
                # path_read:读取dicom的文件路径  path_save:保存nii的文件路径
                def dcm2nii(path_read, path_save):  # from CSDN;function: transfer dcm_series into nii file
                    # GetGDCMSeriesIDs读取序列号相同的dcm文件
                    print("path_read:", path_read)

                    series_id = sitk.ImageSeriesReader.GetGDCMSeriesIDs(path_read)
                    print("series_id:", series_id)

                    # GetGDCMSeriesFileNames读取序列号相同dcm文件的路径，series[0]代表第一个序列号对应的文件
                    series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(path_read, series_id[0])
                    print("series_file_names:",series_file_names)
                    # print(len(series_file_names))  #11
                    series_reader = sitk.ImageSeriesReader()
                    series_reader.SetFileNames(series_file_names)
                    image3d = series_reader.Execute()
                    sitk.WriteImage(image3d, path_save)

                path_save = tmp_save_path + "\\" + every_DCE_series + ".nii"
                if os.path.exists(path_save):
                    continue
                dcm2nii(all_dicoms, path_save)  # 调用函数执行
if __name__ =="__main__":
    folderPath =r"D:\jiazhuangxian"
    savefolder = r"D:\jzx_tmp\NII"
    dicom2Nii(folderPath,savefolder)