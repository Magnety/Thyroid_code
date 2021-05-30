import os, sys

path1 = 'D:\\ThyroidProject\\Data\\raw\\0423\\甲状腺工作站病例收集\\甲状腺良性肿瘤'  # 所需修改文件夹所在路径
dirs = os.listdir(path1)

i = 1
for dir in dirs:
    os.rename(os.path.join(path1,str(dir)),os.path.join(path1,str(i)) )
    print("重命名成功!")
    i += 1
# 打印出重命名后的目录
print("目录为: %s" % os.listdir(os.getcwd()))
