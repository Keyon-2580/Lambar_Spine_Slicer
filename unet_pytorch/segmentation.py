from torch.utils.data import Dataset,DataLoader
import torch
import nibabel as nib
import numpy as np
import SimpleITK as sitk
from scipy import ndimage
import demo.test as test
from unet_pytorch.Unet import UNet, RecombinationBlock



MIN_BOUND = 400.0
MAX_BOUND = -500.0
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

class DataSet(Dataset):
    def __init__(self,n_labels,resize_scale,dataset_path):

        self.dataset_path = dataset_path
        self.resize_scale = resize_scale
        self.n_labels = n_labels


    def __getitem__(self, index):
        data = self.next_train_batch_3d_sub_by_index(resize_scale=self.resize_scale)

        # data = data.transpose(0, 4, 1, 2, 3)
        # target = target.transpose(0, 4, 1, 2, 3)
        return torch.from_numpy(data)

    def __len__(self):
       return len('1')


    def get_np_data_3d(self, resize_scale=1):
        data_np = sitk_read_row(self.dataset_path ,
                                resize_scale=resize_scale)

        data_np=norm_img(data_np)

        return data_np

    def next_train_batch_3d_sub_by_index(self, resize_scale=1):

        img= self.get_np_data_3d(resize_scale=resize_scale)
        train_imgs = np.zeros([1, img.shape[0], img.shape[1], img.shape[2]])
        train_imgs[0] = img
        return train_imgs


def test(model, test_loader,sliced_path):
    print("Evaluation of Testset Starting...")
    model.eval()
    #开始处理
    with torch.no_grad():
        for data in (test_loader):
            data = data.float()
            data  = data.to(device)
            a = int(data.shape[2] / 16)
            #分块处理
            output = torch.zeros((1,4,16*a,data.shape[3],data.shape[4]),dtype=torch.float64)
            for i in range(a):
                for j in range(2):
                    for k in range(2):
                        datax = data [:,:, i*16:(i+1)*16, j*128:(j+1)*128, k*128:(k+1)*128]
                        output_0 = model(datax)
                        #合块#
                        output[:,:,i * 16:(i + 1) * 16, j * 128:(j + 1) * 128, k * 128:(k + 1) * 128] = output_0
            #处理维度并保存
            output = torch.squeeze(output)
            output = torch.argmax(output, dim=0)
            output = output.numpy()
            print(output.shape)
            array_img = nib.Nifti1Image(output, np.eye(4))
            nib.save(array_img, sliced_path + '/sliced_file.nii.gz' )


def segmentation(path,sliced_path):
    test_set = DataSet(4, 0.5, path)
    test_loader = DataLoader(dataset=test_set, batch_size=1, num_workers=1, shuffle=False)
    model = torch.load('/home/sxchongya/unet_pytorch/output/model-625-1.pth').to(device)
    test(model, test_loader,sliced_path)