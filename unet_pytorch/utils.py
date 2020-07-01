import numpy as np
import random
import SimpleITK as sitk
from scipy import ndimage

MIN_BOUND = 400.0
MAX_BOUND = -500.0

def norm_img(image):
    image = 1*(image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    image[image > 1] = 1.
    image[image < 0] = 0.
    return image


def sitk_read_row(img_path, resize_scale=1):
    nda = sitk.ReadImage(img_path)
    nda = sitk.GetArrayFromImage(nda)  # channel first
    nda=ndimage.zoom(nda,[resize_scale,resize_scale,resize_scale],order=0)
    return nda


def make_one_hot_3d(x, n):
    one_hot = np.zeros([x.shape[0], x.shape[1], x.shape[2], n])
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            for v in range(x.shape[2]):
                one_hot[i, j, v, int(x[i, j, v])] = 1

    return one_hot

def load_file_name_list(file_path):
    file_name_list = []
    with open(file_path, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline().strip()  # 整行读取数据
            if not lines:
                break
                pass
            file_name_list.append(lines)
            pass
    return file_name_list


def random_crop_2d(img, label, crop_size):
    random_x_max = img.shape[0] - crop_size[0]
    random_y_max = img.shape[1] - crop_size[1]

    if random_x_max < 0 or random_y_max < 0:
        return None

    x_random = random.randint(0, random_x_max)
    y_random = random.randint(0, random_y_max)

    crop_img = img[x_random:x_random + crop_size[0], y_random:y_random + crop_size[1]]
    crop_label = label[x_random:x_random + crop_size[0], y_random:y_random + crop_size[1]]

    return crop_img, crop_label


def random_crop_3d(img, label, crop_size):
    random_x_max = img.shape[0] - crop_size[0]
    random_y_max = img.shape[1] - crop_size[1]
    random_z_max = img.shape[2] - crop_size[2]

    if random_x_max < 0 or random_y_max < 0 or random_z_max < 0:
        return None

    x_random = random.randint(0, random_x_max)
    y_random = random.randint(0, random_y_max)
    z_random = random.randint(0, random_z_max)

    crop_img = img[x_random:x_random + crop_size[0], y_random:y_random + crop_size[1], z_random:z_random + crop_size[2]]
    crop_label = label[x_random:x_random + crop_size[0], y_random:y_random + crop_size[1],
                 z_random:z_random + crop_size[2]]
    # crop_img = img
    # crop_label = label


    return crop_img, crop_label

def adjust_learning_rate(optimizer, epoch, args):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    lr = args.lr * (0.1 ** (epoch // 30))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr




