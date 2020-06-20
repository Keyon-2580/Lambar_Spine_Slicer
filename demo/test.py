import glob
import os
from test_002 import settings
#
# WSI_MASK_PATH = 'F:\\大三下\\Lumbar'#存放图片的文件夹路径
# paths = glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg'))
# paths.sort()
# print(settings.IMAGE_ROOT )


import numpy as np
import os  # 遍历文件夹
import nibabel as nib  # nii格式一般都会用到这个包
import imageio  # 转换成图像


def nii_to_image(niifile):
    filenames = os.listdir(filepath)  # 读取nii文件夹
    slice_trans = []

    for f in filenames:
        # 开始读取nii文件
        img_path = os.path.join(filepath, f)
        img = nib.load(img_path)  # 读取nii
        img_fdata = img.get_fdata()
        fname = f.replace('.nii', '')  # 去掉nii的后缀名
        img_f_path = os.path.join(imgfile, fname)
        # 创建nii对应的图像的文件夹
        if not os.path.exists(img_f_path):
            os.mkdir(img_f_path)  # 新建文件夹

        # 开始转换为图像
        (x, y, z) = img.shape
        for i in range(z):  # z是图像的序列
            silce = img_fdata[i, :, :]  # 选择哪个方向的切片都可以
            imageio.imwrite(os.path.join(img_f_path, '{}.png'.format(i)), silce)
            # 保存图像


if __name__ == '__main__':
    filepath = 'F:\\大三下\\项目实训\\腰椎项目实训资料Part1\\' \
               '腰椎项目实训资料Part1\\腰椎数据样例\\184.XieTongQing\\分割网络可读入的数据格式' \
               '\\2 0.625MM.nii'
    imgfile = 'F:\\大三下\\Lumbar\\image_nii'
    nii_to_image(filepath)