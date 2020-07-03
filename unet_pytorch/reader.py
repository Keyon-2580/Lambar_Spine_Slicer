import numpy as np
import os
import glob

import random
from utils import *
import config



'''
def sitk_read(img_path):
    nda = sitk.ReadImage(img_path)
    nda = sitk.GetArrayFromImage(nda) #(155,240,240)
    zero = np.zeros([5, 240, 240])
    nda = np.concatenate([zero, nda], axis=0) #(160,240,240)
    nda = nda.transpose(1, 2, 0) #(240,240,160)
    return nda
'''

class Reader:
    def __init__(self, data_init=False, data_fix=False):
        self.row_root_path = r'/home/File/LumbarData/nii.gz格式数据/'
        self.data_root_path = r'fixed'

        if not os.path.exists(self.data_root_path):  # 创建保存目录
            os.makedirs(os.path.join(self.data_root_path,'data'))
            os.makedirs(os.path.join(self.data_root_path,'label'))

        if data_init:
            self.init_data()
        if data_fix:
            self.fix_data()

        self.train_name_list = load_file_name_list(os.path.join(self.data_root_path, "train_name_list.txt"))
        self.val_name_list = load_file_name_list(os.path.join(self.data_root_path, 'val_name_list.txt'))
        self.test_name_list = load_file_name_list(os.path.join(self.data_root_path, 'val_name_list.txt'))

        self.n_train_file = len(self.train_name_list)
        self.n_val_file = len(self.val_name_list)
        self.n_test_file = len(self.test_name_list)

        self.train_batch_index = 0
        self.val_batch_index = 0
        self.test_batch_index = 0

        self.n_labels = config.args.class_num

    def write_train_val_test_name_list(self):
        data_name_list = os.listdir(os.path.join(self.data_root_path, "data"))
        data_num = len(data_name_list)

        random.shuffle(data_name_list)
        n_train_file = int(data_num / 10 * 8)
        n_val_file = int(data_num / 10 * 1)
        train_name_list = data_name_list[0:n_train_file]
        val_name_list = data_name_list[n_train_file:(n_train_file + n_val_file)]
        test_name_list = data_name_list[(n_train_file + n_val_file):len(data_name_list)]
        self.write_name_list(train_name_list, "train_name_list.txt")
        self.write_name_list(val_name_list, "val_name_list.txt")
        self.write_name_list(test_name_list, "test_name_list.txt")

    def write_name_list(self, name_list, file_name):
        f = open(os.path.join(self.data_root_path ,file_name), 'w')
        for i in range(len(name_list)):
            f.write(str(name_list[i]) + "\n")
        f.close()

    def init_data(self):
        self.write_train_val_test_name_list()

    def fix_data(self):

        expand_slice = 20  # 轴向上向外扩张的slice数量
        size = 48  # 取样的slice数量

        row_data_path = os.path.join(self.row_root_path, 'imagesTr')
        row_seg_path = os.path.join(self.row_root_path, 'labelsTr')
        fixed_data_path = os.path.join(self.data_root_path, 'data')
        fixed_seg_path = os.path.join(self.data_root_path, 'label')
        row_data_ls = os.listdir(row_data_path)
        for ct_file in row_data_ls:

            print(ct_file)
            # 将CT和金标准入读内存
            ct = sitk.ReadImage(os.path.join(row_data_path, ct_file), sitk.sitkInt16)
            ct_array = sitk.GetArrayFromImage(ct)

            seg = sitk.ReadImage(os.path.join(row_seg_path, ct_file),
                                 sitk.sitkInt8)
            seg_array = sitk.GetArrayFromImage(seg)

            print(ct_array.shape, seg_array.shape)


            # 将灰度值在阈值之外的截断掉
            ct_array[ct_array > 400] = 400
            ct_array[ct_array < -500] = -500

            # 找到开始和结束的slice，并各向外扩张
            z = np.any(seg_array, axis=(1, 2))
            start_slice, end_slice = np.where(z)[0][[0, -1]]

            # 两个方向上各扩张个slice
            if start_slice - expand_slice < 0:
                start_slice = 0
            else:
                start_slice -= expand_slice

            if end_slice + expand_slice >= seg_array.shape[0]:
                end_slice = seg_array.shape[0] - 1
            else:
                end_slice += expand_slice

            print(str(start_slice) + '--' + str(end_slice))


            ct_array = ct_array[start_slice:end_slice + 1:]
            seg_array = sitk.GetArrayFromImage(seg)
            seg_array = seg_array[start_slice:end_slice + 1]

            new_ct = sitk.GetImageFromArray(ct_array)
            new_seg = sitk.GetImageFromArray(seg_array)

            sitk.WriteImage(new_ct, os.path.join(fixed_data_path, ct_file.replace('spine1_', 'volume-')))
            sitk.WriteImage(new_seg,
                            os.path.join(fixed_seg_path, ct_file.replace('spine1_', 'segmentation-')))




def main():
    reader = Reader(data_init=True,data_fix=True)
    #img, label = reader.next_val_batch_3d_sub(8, [32, 64, 64])
    #print(img.shape)
    #print(label.shape)


if __name__ == '__main__':
    main()
