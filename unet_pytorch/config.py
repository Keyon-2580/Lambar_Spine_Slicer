import argparse


parser = argparse.ArgumentParser(description='3DUNet')

parser.add_argument('--class_num',default=4,
                    help='class_num')
parser.add_argument('--epochs', type=int, default=200, metavar='N',
                    help='number of epochs to train (default: 10)')
parser.add_argument('--lr', type=float, default=0.02, metavar='LR',
                    help='learning rate (default: 0.01)')
parser.add_argument('--momentum', type=float, default=0.8, metavar='M',
                    help='SGD momentum (default: 0.5)')
parser.add_argument('--save-model', action='store_true', default=False,
                    help='For Saving the current Model')
parser.add_argument('--data_path', default=r'fixed',
                    help='fixed trainset root path')
parser.add_argument('--crop_size', type=list, default=[16, 128, 128],
                    help='patch size of train samples after resize')
parser.add_argument('--batch_size', type=list, default=4,
                    help='batch size of trainset')
parser.add_argument('--resize_scale', type=float, default=1,
                    help='resize scale for input data')
parser.add_argument('--dataset_path',default=r'fixed',
                    help='fixed trainset root path')
parser.add_argument('--model_path',default=r'output/model-628-2.pth',
                    help='model path')
parser.add_argument('--n_threads', type=int, default=10,
                    help='number of threads for data loading')

args = parser.parse_args()