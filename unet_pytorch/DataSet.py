import numpy as np
from torchvision import transforms as T
import torch
from torch.utils.data import Dataset, DataLoader
import reader
import config
import os
from utils import *
import config




class DataSet(Dataset):
    def __init__(self,n_labels, crop_size,resize_scale,dataset_path,mode=None):
        self.crop_size = crop_size
        self.dataset_path = dataset_path
        self.resize_scale = resize_scale
        self.n_labels = n_labels
        if mode=='train':
            self.filename_list = load_file_name_list(os.path.join(dataset_path,'train_name_list.txt'))
        elif mode =='val':
            self.filename_list = load_file_name_list(os.path.join(dataset_path, 'val_name_list.txt'))
        elif mode == 'test':
            self.filename_list = load_file_name_list(os.path.join(dataset_path, 'test_name_list.txt'))
        else:
            raise TypeError('Dataset mode error!!! ')

    def __getitem__(self, index):
        data, target = self.next_train_batch_3d_sub_by_index(crop_size=self.crop_size, index=index,
                                                            resize_scale=self.resize_scale)

        # data = data.transpose(0, 4, 1, 2, 3)
        # target = target.transpose(0, 4, 1, 2, 3)
        return torch.from_numpy(data), torch.from_numpy(target)

    def __len__(self):
        return len(self.filename_list)

    def get_np_data_3d(self, data_name, resize_scale=1):
        data_np = sitk_read_row(self.dataset_path + '/data/' + data_name,
                                resize_scale=resize_scale)

        data_np=norm_img(data_np)
        label_np = sitk_read_row(self.dataset_path + '/label/' + data_name.replace('volume', 'segmentation'),
                                 resize_scale=resize_scale)

        label_np[label_np > config.args.class_num-1] = 0

        return data_np, label_np

    def next_train_batch_3d_sub_by_index(self,crop_size, index, resize_scale=1):

        # #train_imgs = np.zeros([1, crop_size[0], crop_size[1], crop_size[2]])
        #
        # #train_labels = np.zeros([1, crop_size[0], crop_size[1], crop_size[2], self.n_labels])
        # img, label = self.get_np_data_3d(self.filename_list[index],resize_scale=resize_scale)
        # train_imgs = np.zeros([1, img.shape[0], img.shape[1], img.shape[2]])
        # sub_img, sub_label = random_crop_3d(img, label, crop_size)
        #
        # sub_label_onehot = make_one_hot_3d(label, self.n_labels)
        #
        # train_labels = sub_label_onehot.transpose(3, 0, 1, 2)
        # train_imgs[0] = img
        # return train_imgs, train_labels


        train_imgs = np.zeros([1, crop_size[0], crop_size[1], crop_size[2]])
        # train_labels = np.zeros([1, crop_size[0], crop_size[1], crop_size[2], self.n_labels])
        img, label = self.get_np_data_3d(self.filename_list[index], resize_scale=resize_scale)

        sub_img, sub_label = random_crop_3d(img, label, crop_size)
        sub_label_onehot = make_one_hot_3d(sub_label, self.n_labels)
        train_labels = sub_label_onehot.transpose(3, 0, 1, 2)
        train_imgs[0] = sub_img

        return train_imgs, train_labels


