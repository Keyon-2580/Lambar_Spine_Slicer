from DataSet import *
from torch.utils.data import DataLoader
import torch
import torch.optim as optim
from tqdm import tqdm
import config
from Unet import UNet, RecombinationBlock,ResBlock
from utils import *
import metrics
import SimpleITK as sitk
import nibabel as nib



def test(model, test_loader):
    print("Evaluation of Testset Starting...")
    model.eval()
    val_loss = 0
    val_dice0 = 0
    val_dice1 = 0
    val_dice2 = 0
    val_dice3 = 0
    m = 0
    with torch.no_grad():
        # total_data = np.zeros((96,256,256),dtype = np.float64)
        # total_data_1 = np.zeros((16, 128, 128), dtype=np.float64)
        for data, target in tqdm(test_loader):
            data, target = data.float(), target.float()
            data, target = data.to(device), target.to(device)
            a = int(data.shape[2] / 16)
            #total_data = np.zeros((1, 1, 16*a, data.shape[3], data.shape[4]))
            output = torch.zeros((1,4,16*a,data.shape[3],data.shape[4]),dtype=torch.float64)
            for i in range(a):
                for j in range(2):
                    for k in range(2):
                        datax = data [:,:, i*16:(i+1)*16, j*128:(j+1)*128, k*128:(k+1)*128]
                        output_0 = model(datax)
                        #output_0 = output_0.cuda().data.cpu().numpy()
                        output[:,:,i * 16:(i + 1) * 16, j * 128:(j + 1) * 128, k * 128:(k + 1) * 128] = output_0



            #output = model(data)
            # i = 0
            # n = 0
            # m = 0
            # print(target.shape)
            # for a in range(16):
            #     for b in range(128):
            #         for c in range(128):
            #             if (target[0, 2, a, b, c] > 0.5):
            #                 i += 1
            #             elif (target[0, 1, a, b, c] > 0.5):
            #                 m += 1
            #             elif (target[0, 3, a, b, c] > 0.5):
            #                 n += 1
            # print(i)
            # print(m)
            # print(n)

            #target = torch.squeeze(target)

            # print(data.shape)
            # for a in range(96):
            #     for b in range(256):
            #         for c in range(256):
            #             if (data[0,0, a, b, c] != 0):
            #                 print(data[0,0, a, b, c])
            #
            # for i in range(6):
            #     for j in range(2):
            #         for k in range(2):
            #             datax = data [:,:, i*16:(i+1)*16, j*128:(j+1)*128, k*128:(k+1)*128]
            #             output = model(datax)
            #             #output = torch.argmax(output, dim=0)
            #             output = torch.squeeze(output)
            #             #output = torch.argmax(output, dim=0)
            #             for d in range(4):
            #                 for a in range(16):
            #                     for b in range(128):
            #                         for c in range(128):
            #                             #print(output[d,a,b,c])
            #                             if(output[d,a,b,c] == 1):
            #                                 #total_data_1[a,b,c] = d
            #                                 #print(d)
            #                                 continue
            #                             else:
            #                                 break
                        #total_data_1 = total_data_1.cuda().data.cpu().numpy()
                        #total_data[i * 16:(i + 1) * 16, j * 128:(j + 1) * 128, k * 128:(k + 1) * 128] = total_data_1

            # for a in range(16):
            #     for b in range(128):
            #         for c in range(128):
            #             if (output[0, 2, a, b, c] > 0.5):
            #                 total_data[a,b,c] = 2
            #             elif (output[0, 1, a, b, c] > 0.5):
            #                 total_data[a,b,c] = 1
            #             elif (output[0, 3, a, b, c] > 0.5):
            #                 total_data[a,b,c] = 3


            # print(output.shape)
            # print(target.shape)
            # loss = metrics.DiceMeanLoss()(output, target)
            # dice0 = metrics.dice(output, target, 0)
            # dice1 = metrics.dice(output, target, 1)
            # dice2 = metrics.dice(output, target, 2)
            # dice3 = metrics.dice(output, target, 3)
            #
            # val_loss += float(loss)
            # val_dice0 += float(dice0)
            # val_dice1 += float(dice1)
            # val_dice2 += float(dice2)
            # val_dice3 += float(dice3)
            #output = torch.from_numpy(output)
            output = torch.squeeze(output)
            output = torch.argmax(output, dim=0)
            output = output.numpy()
            print(output.shape)
            array_img = nib.Nifti1Image(output, np.eye(4))
            nib.save(array_img, '/home/sxchongya/unet_pytorch/fixed/mask_%d.nii.gz' % m)
            m += 1



    val_loss /= len(test_loader)
    val_dice0 /= len(test_loader)
    val_dice1 /= len(test_loader)
    val_dice2 /= len(test_loader)
    val_dice3 /= len(test_loader)

    print('\nTest set: Average loss: {:.6f},\tdice0: {:.6f}\tdice1: {:.6f}\tdice2: {:.6f}\tdice3: {:.6f}\n'.format(
        val_loss, val_dice0, val_dice1, val_dice2, val_dice3))


if __name__ == '__main__':
    args = config.args
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # data info

    test_set = DataSet(args.class_num,args.crop_size, args.resize_scale, args.dataset_path, mode='test')
    test_loader = DataLoader(dataset=test_set,batch_size=args.batch_size,num_workers=1, shuffle=False)

    # model info
    # model = UNet(1, [32, 48, 64, 96, 128], 3, net_mode='3d',conv_block=RecombinationBlock).to(device)
    # model.load_state_dict(torch.load('./output/{}/state.pkl'.format(args.save)))
    # model = torch.load(args.model_path).to(device)
    # print(model)
    model = UNet(1, [32, 48, 64, 96, 128], args.class_num, net_mode='3d',conv_block=ResBlock).to(device)
    model.load_state_dict(torch.load('output/model-628-1.pth'))
    print(model)
    model.eval()
    test(model, test_loader)
    #img = sitk.ReadImage('/home/sxchongya/unet_pytorch/fixed/data/volume-5.nii.gz')
    #f = sitk.GetArrayFromImage(img)
    #f = torch.tensor(f)
    #x = torch.rand(4, 1, 64, 96, 96)
    #x = x.to(device)
    #res = model.forward(x)

    #print(res)