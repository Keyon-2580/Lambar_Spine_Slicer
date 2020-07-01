import os  # 遍历文件夹
import nibabel as nib  # nii格式一般都会用到这个包
import imageio  # 转换成图像
from PIL import Image
import numpy as np
import nrrd
import os
import imageio
import zipfile
import pydicom
import SimpleITK as sitk



filepath = '/home/sxchongya/original_file/temporary'
imgfile = '/home/sxchongya/original_files/temporary'


def nii_to_image(niifile,code,id):
    if(code == 0):
        filepath = '/home/sxchongya/original_file/temporary'
        imgfile = '/home/sxchongya/original_files/temporary'
    elif(code == 1):
        filepath = '/home/sxchongya/original_files/'+id+'/'
        imgfile = '/home/sxchongya/original_files/'+id+'/'
    # 开始读取nii文件
    img_path = os.path.join(filepath, niifile)

    img = nib.load(img_path)  # 读取nii
    img_fdata = img.get_fdata()
    fname = niifile.replace('.nii.gz', '')  # 去掉nii的后缀名

    img_f_path_x = os.path.join(imgfile, fname + 'x')
    img_f_path_y = os.path.join(imgfile, fname + 'y')
    img_f_path_z = os.path.join(imgfile, fname + 'z')

    # 创建nii对应的图像的文件夹
    if not os.path.exists(img_f_path_x):
        os.mkdir(img_f_path_x)
    if not os.path.exists(img_f_path_y):
        os.mkdir(img_f_path_y)
    if not os.path.exists(img_f_path_z):
        os.mkdir(img_f_path_z)

    (x, y, z) = img.shape
    for i in range(x):
        silce = img_fdata[i, :, :]
        imageio.imwrite(os.path.join(img_f_path_x, '{}.png'.format(i)), silce)
    for i in range(y):
        silce = img_fdata[:, i, :]
        imageio.imwrite(os.path.join(img_f_path_y, '{}.png'.format(i)), silce)
    for i in range(z):
        silce = img_fdata[:, :, i]
        imageio.imwrite(os.path.join(img_f_path_z, '{}.png'.format(i)), silce)


def nrrd_to_image(nrrd_filename):
    img_path = os.path.join(filepath, nrrd_filename)
    print(img_path)
    nrrd_data, nrrd_options = nrrd.read(img_path)
    img=nrrd_options
    fname = nrrd_filename.replace('.seg.nrrd', '')
    img_f_path_x = os.path.join(imgfile, fname + 'x')
    img_f_path_y = os.path.join(imgfile, fname + 'y')
    img_f_path_z = os.path.join(imgfile, fname + 'z')
    if not os.path.exists(img_f_path_x):
        os.mkdir(img_f_path_x)
    if not os.path.exists(img_f_path_y):
        os.mkdir(img_f_path_y)
    if not os.path.exists(img_f_path_z):
        os.mkdir(img_f_path_z)
    a = nrrd_options
    h = 0
    for key in a:
        if h == 3:
            c = a[key]
        h += 1
    x=c[0]
    y=c[1]
    z=c[2]
    for i in range(x):
        # [i, :, :]
        nrrd_image = (nrrd_data[i, :, :] * 1.5)
        imageio.imwrite(os.path.join(img_f_path_x, '{}.png'.format(i)), nrrd_image)
    for i in range(y):
        nrrd_image = (nrrd_data[:, i, :] * 1.5)
        imageio.imwrite(os.path.join(img_f_path_y, '{}.png'.format(i)), nrrd_image)
    for i in range(z):
        nrrd_image = (nrrd_data[:, :, i] * 1.5)
        imageio.imwrite(os.path.join(img_f_path_z, '{}.png'.format(i)), nrrd_image)


path_0='/home/sxchongya/original_file/temporary'
# 存放解压后的dicom
folder_abs='/home/sxchongya/original_file/temporary'
# 存放照片png
imgfile = '/home/sxchongya/original_files/temporary'
def dicomtoimg(file):
    path_0 = '/home/sxchongya/original_file/temporary'
    # 存放解压后的dicom
    folder_abs = '/home/sxchongya/original_file/temporary'
    # 存放照片png
    imgfile = '/home/sxchongya/original_files/temporary'
    path = os.path.join(path_0,file)
    zip_file = zipfile.ZipFile(path,'r')
    zip_list = zip_file.namelist()  # 得到压缩包里所有文件
    y=folder_abs
    folder_abs=folder_abs+zip_list[0]
    i={}
    j=0
    for f in zip_list:
        zip_file.extract(f, y)  # 循环解压文件到指定目录
        i[j]=y+'/'+f
        j=j+1
    zip_file.close()  # 关闭文件，必须有，释放内存
    PathDicom=i[0]
    lstFilesDCM = []
    for dirName,subdirList,fileList in os.walk(PathDicom):
        for filename in fileList:
            if ".dcm" in filename.lower():  # 判断文件是否
            # print(filename)
                lstFilesDCM.append(os.path.join(dirName, filename))
    print(len(lstFilesDCM))
    file_len=len(lstFilesDCM)
    frame='img'
    filepath =PathDicom
    dicomname=[None]*file_len
    fname=file.replace('.zip','')
    img_f_path_x = os.path.join(imgfile, fname+'z')
    if not os.path.exists(img_f_path_x):
        os.mkdir(img_f_path_x)
    for k in range(file_len):
        dicomname[k]=lstFilesDCM[k]
        # print(dicomname[k])
    for k in range(file_len):
        ds = sitk.ReadImage(dicomname[k])
        img_array = sitk.GetArrayFromImage(ds)
        slice=img_array[0,:,:]
        imageio.imwrite(os.path.join(img_f_path_x, '{}.png'.format(k)), slice)