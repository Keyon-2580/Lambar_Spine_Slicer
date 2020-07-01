from DataSet import *
import torch
import argparse
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
from reader import *
import metrics
from torch.utils.data import Dataset, DataLoader
from Unet import UNet,ResBlock,RecombinationBlock
import logger
import init_util
import config


def val(model, val_loader, device, epoch, val_dict, logger):
    model.eval()
    val_loss = 0
    val_dice0 = 0
    val_dice1 = 0
    val_dice2 = 0
    val_dice3 = 0
    with torch.no_grad():
        for data, target in val_loader:
            data = torch.squeeze(data, dim=0)
            target = torch.squeeze(target, dim=0)
            data, target = data.float(), target.float()
            data, target = data.to(device), target.to(device)
            output = model(data)

            loss = metrics.DiceMeanLoss()(output, target)
            #loss = metrics.SoftDiceLoss()(output, target)
            dice0 = metrics.dice(output, target, 0)
            dice1 = metrics.dice(output, target, 1)
            dice2 = metrics.dice(output, target, 2)
            dice3 = metrics.dice(output, target, 3)

            val_loss += float(loss)
            val_dice0 += float(dice0)
            val_dice1 += float(dice1)
            val_dice2 += float(dice2)
            val_dice3 += float(dice3)

    val_loss /= len(val_loader)
    val_dice0 /= len(val_loader)
    val_dice1 /= len(val_loader)
    val_dice2 /= len(val_loader)
    val_dice3 /= len(val_loader)

    val_dict['loss'].append(float(val_loss))
    val_dict['dice0'].append(float(val_dice0))
    val_dict['dice1'].append(float(val_dice1))
    val_dict['dice2'].append(float(val_dice2))
    val_dict['dice3'].append(float(val_dice3))
    logger.scalar_summary('val_loss', val_loss, epoch)
    logger.scalar_summary('val_dice0', val_dice0, epoch)
    logger.scalar_summary('val_dice1', val_dice1, epoch)
    logger.scalar_summary('val_dice2', val_dice2, epoch)
    logger.scalar_summary('val_dice3', val_dice3, epoch)
    print('\nVal set: Average loss: {:.6f}, dice0: {:.6f}\tdice1: {:.6f}\tdice2: {:.6f}\tdice3: {:.6f}\t\n'.format(
        val_loss, val_dice0,val_dice1, val_dice2, val_dice3))


def train(model, train_loader, device, optimizer, epoch, train_dict, logger):
    model.train()
    train_loss = 0
    train_dice0 = 0
    train_dice1 = 0
    train_dice2 = 0
    train_dice3 = 0
    for batch_idx, (data, target) in enumerate(train_loader):
        data = torch.squeeze(data, dim=0)
        target = torch.squeeze(target, dim=0)
        data, target = data.float(), target.float()
        data, target = data.to(device), target.to(device)
        output = model(data)

        optimizer.zero_grad()

        # loss = nn.CrossEntropyLoss()(output,target)
        #loss=metrics.SoftDiceLoss()(output,target)
        # loss=nn.MSELoss()(output,target)
        loss = metrics.DiceMeanLoss()(output, target)
        # loss=metrics.WeightDiceLoss()(output,target)
        # loss=metrics.CrossEntropy()(output,target)
        loss.backward()
        optimizer.step()

        train_loss = loss
        train_dice0 = metrics.dice(output, target, 0)
        train_dice1 = metrics.dice(output, target, 1)
        train_dice2 = metrics.dice(output, target, 2)
        train_dice3 = metrics.dice(output, target, 3)
        print(
            'Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\tdice0: {:.6f}\tdice1: {:.6f}\tdice2: {:.6f}\tdice3: {:.6f}\tT: {:.6f}\tP: {:.6f}\tTP: {:.6f}'.format(
                epoch, batch_idx, len(train_loader),
                100. * batch_idx / len(train_loader), loss.item(),
                train_dice0,train_dice1, train_dice2, train_dice3,
                metrics.T(output, target), metrics.P(output, target), metrics.TP(output, target)))

    train_dict['loss'].append(float(train_loss))
    train_dict['dice0'].append(float(train_dice0))
    train_dict['dice1'].append(float(train_dice1))
    train_dict['dice2'].append(float(train_dice2))
    train_dict['dice3'].append(float(train_dice3))

    logger.scalar_summary('train_loss', train_loss, epoch)
    logger.scalar_summary('train_dice0', train_dice0, epoch)
    logger.scalar_summary('train_dice1', train_dice1, epoch)
    logger.scalar_summary('train_dice2', train_dice2, epoch)
    logger.scalar_summary('train_dice3', train_dice3, epoch)



if __name__ == '__main__':
    # torch.cuda.set_device(3)
    args = config.args
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # PyTorch v0.4.0
    model = UNet(1, [48, 64, 96, 128, 256], args.class_num, net_mode='3d',conv_block=ResBlock).to(device)
    init_util.print_network(model)

    # model = nn.DataParallel(model, device_ids=[0, 1])  # multi-GPU

    reader = Reader(data_fix=False)
    train_set = DataSet(args.class_num, args.crop_size, args.resize_scale, args.dataset_path, mode='train')
    val_set = DataSet(args.class_num, args.crop_size, args.resize_scale, args.dataset_path, mode='val')
    train_loader = DataLoader(dataset=train_set, batch_size=args.batch_size, num_workers=int(args.n_threads / 2),
                              shuffle=True)
    val_loader = DataLoader(dataset=val_set, batch_size=args.batch_size, num_workers=int(args.n_threads / 2),
                            shuffle=True)

    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)

    train_dict = {'loss': [], 'dice0': [], 'dice1': [], 'dice2': [], 'dice3': []}
    val_dict = {'loss': [], 'dice0': [], 'dice1': [], 'dice2': [], 'dice3': []}

    logger = logger.Logger('./log')
    for epoch in range(1, args.epochs + 1):
        adjust_learning_rate(optimizer, epoch, args)
        train(model, train_loader, device, optimizer, epoch, train_dict, logger)
        val(model, val_loader, device, epoch, val_dict, logger)
        torch.save(model.state_dict(), args.model_path)