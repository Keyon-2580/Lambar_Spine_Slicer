import xml.etree.ElementTree as etree
from svg.path import parse_path
import numpy as np
import nibabel as nib
import cv2


#=======svg文件路径，nii文件路径，切片索引，保存路径===========
def lasso(svgpath,niipath,index,savepath):
    target = etree.parse(svgpath)
    paths = target.findall("{http://www.w3.org/2000/svg}path")
    sjg = []
    zjp = []
    ymn = []
    for path in paths:
        color = path.attrib['style'][12:19:1]
        ps = parse_path(path.attrib['d'])
        if color == '255,0,0':
            for p in ps:
                if p.length() == 0:
                    continue
                sjg.append([int(p.start.real),int(p.start.imag)])
        if color == '0,128,0':
            for p in ps:
                if p.length() == 0:
                    continue
                zjp.append([int(p.start.real),int(p.start.imag)])
        if color == '0,0,255':
            for p in ps:
                if p.length() == 0:
                    continue
                ymn.append([int(p.start.real),int(p.start.imag)])
    sjg = np.array(sjg)
    zjp = np.array(zjp)
    ymn = np.array(ymn)
#====================================================================

    img = nib.load(niipath).dataobj
    img = np.array(img)

    #print(img.shape)
    #current = img[:,:,index]
    current = np.zeros((512,512))

    #=========================神经根==============================
    print(sjg.shape)
    amount, a = sjg.shape
    #print(amount)
    # 获取套索轮廓上的所有像素
    sjgp = []
    for i in range(amount):
        # print(sjg[i][0])
        if i <= amount - 2:
            x1 = sjg[i][0]
            y1 = sjg[i][1]
            x2 = sjg[i + 1][0]
            y2 = sjg[i + 1][1]
            if x2 == x1:
                k = (y2 - y1)
            else:
                k = (y2 - y1) / (x2 - x1)  # 斜率k
            b = y1 - k * x1  # 参数b
            # 求交点
            dur = abs(x2 - x1) + 1
            if x2 > x1:
                for each in range(dur):
                    x = x1 + each
                    y = k * x + b
                    sjgp.append([int(x), int(y)])
            else:
                for each in range(dur):
                    x = x2 + each
                    y = k * x + b
                    sjgp.append([int(x), int(y)])
        else:
            x1 = sjg[i][0]
            y1 = sjg[i][1]
            x2 = sjg[0][0]
            y2 = sjg[0][1]
            if x2 == x1:
                k = (y2 - y1)
            else:
                k = (y2 - y1) / (x2 - x1)  # 斜率k
            b = y1 - k * x1  # 参数b
            # 求交点
            dur = abs(x2 - x1) + 1
            if x2 > x1:
                for each in range(dur):
                    x = x1 + each
                    y = k * x + b
                    sjgp.append([int(x), int(y)])
            else:
                for each in range(dur):
                    x = x2 + each
                    y = k * x + b
                    sjgp.append([int(x), int(y)])
    sjgp = np.array(sjgp)
    #print(sjgp)
    sjgp = sjgp[np.lexsort(sjgp[:, :-1].T)]
    #print(sjgp)

    # 扫描线算法填充像素
    count, b = sjgp.shape
    #print(count)

    miny = 513
    maxy = -1
    for i in range(count):
        nowx = sjgp[i][0]
        if sjgp[i][1] < miny:
            miny = sjgp[i][1]
        if sjgp[i][1] > maxy:
            maxy = sjgp[i][1]
        if i == count - 1:
            break;
        if sjgp[i][0] != sjgp[i + 1][0]:
            rift = abs(maxy - miny) + 1
            for j in range(rift):
                current[miny + j][nowx] = 60
            miny = 513
            maxy = -1


    #=============================椎间盘==================
    amount, a = zjp.shape
    #print(amount)
    # 获取套索轮廓上的所有像素
    zjpp = []
    for i in range(amount):
        # print(sjg[i][0])
        if i <= amount - 2:
            x1 = zjp[i][0]
            y1 = zjp[i][1]
            x2 = zjp[i + 1][0]
            y2 = zjp[i + 1][1]
            if x2 == x1:
                k = (y2 - y1)
            else:
                k = (y2 - y1) / (x2 - x1)  # 斜率k
            b = y1 - k * x1  # 参数b
            # 求交点
            dur = abs(x2 - x1) + 1
            if x2 > x1:
                for each in range(dur):
                    x = x1 + each
                    y = k * x + b
                    zjpp.append([int(x), int(y)])
            else:
                for each in range(dur):
                    x = x2 + each
                    y = k * x + b
                    zjpp.append([int(x), int(y)])
        else:
            x1 = zjp[i][0]
            y1 = zjp[i][1]
            x2 = zjp[0][0]
            y2 = zjp[0][1]
            if x2 == x1:
                k = (y2 - y1)
            else:
                k = (y2 - y1) / (x2 - x1)  # 斜率k
            b = y1 - k * x1  # 参数b
            # 求交点
            dur = abs(x2 - x1) + 1
            if x2 > x1:
                for each in range(dur):
                    x = x1 + each
                    y = k * x + b
                    zjpp.append([int(x), int(y)])
            else:
                for each in range(dur):
                    x = x2 + each
                    y = k * x + b
                    zjpp.append([int(x), int(y)])
    zjpp = np.array(zjpp)
    zjpp = zjpp[np.lexsort(zjpp[:, :-1].T)]
    #print(zjpp)
    # print(ymnp)

    # 扫描线算法填充像素
    count, b = zjpp.shape
    #print(count)
    miny = 513
    maxy = -1
    for i in range(count):
        nowx = zjpp[i][0]
        if zjpp[i][1] < miny:
            miny = zjpp[i][1]
        if zjpp[i][1] > maxy:
            maxy = zjpp[i][1]
        if i == count - 1:
            break;
        if zjpp[i][0] != zjpp[i + 1][0]:
            rift = abs(maxy - miny) + 1
            for j in range(rift):
                current[miny + j][nowx] = 60
            miny = 513
            maxy = -1

    # =============================硬膜囊=======================
    amount,a = ymn.shape
    #print(amount)
    #获取套索轮廓上的所有像素
    ymnp = []
    for i in range(amount):
        #print(sjg[i][0])
        print(i)
        if i <= amount-2:
            x1 = ymn[i][0]
            y1 = ymn[i][1]
            x2 = ymn[i+1][0]
            y2 = ymn[i+1][1]
            if x2==x1:
                k = (y2-y1)
            else:
                k = (y2 - y1) / (x2 - x1)  # 斜率k
            b = y1 - k*x1        #参数b
            #求交点
            dur = abs(x2-x1)+1
            if x2>x1:
                for each in range(dur):
                    x = x1 + each
                    y = k*x + b
                    ymnp.append([int(x), int(y)])
            else :
                for each in range(dur):
                    x = x2 + each
                    y = k * x + b
                    ymnp.append([int(x), int(y)])
        if i == amount-1:
            x1 = ymn[i][0]
            y1 = ymn[i][1]
            x2 = ymn[0][0]
            y2 = ymn[0][1]
            if x2==x1:
                k = (y2-y1)
            else:
                k = (y2 - y1) / (x2 - x1)  # 斜率k
            b = y1 - k * x1  # 参数b
            # 求交点
            dur = abs(x2-x1)+1
            if x2 > x1:
                for each in range(dur):
                    x = x1 + each
                    y = k * x + b
                    ymnp.append([int(x), int(y)])
            else:
                for each in range(dur):
                    x = x2 + each
                    y = k * x + b
                    ymnp.append([int(x), int(y)])
    ymnp = np.array(ymnp)
    ymnp = ymnp[np.lexsort(ymnp[:, :-1].T)]
    #print(ymnp)
    #print(ymnp)

    #扫描线算法填充像素
    count,b = ymnp.shape
    #print(count)
    miny = 513
    maxy = -1
    for i in range(count):
        nowx = ymnp[i][0]
        if ymnp[i][1] < miny:
            miny = ymnp[i][1]
        if ymnp[i][1] > maxy:
            maxy = ymnp[i][1]
        if i == count -1:
            break;
        if ymnp[i][0] != ymnp[i + 1][0]:
            rift = abs(maxy-miny) + 1
            for j in range(rift):
                current[miny+j][nowx] = 60
            miny = 513
            maxy = -1
    print(img.shape)


    img[:,:,int(index)] = current

    new_image = nib.Nifti1Image(img, np.eye(4))
    nib.save(new_image, savepath)
    img2 = np.array(current, dtype=np.uint8)

    cv2.imshow('test2',img2)
    cv2.waitKey(0)


#======================test==============
# taosuo('kkk.svg','huhulu.nii.gz',0,'haha.nii.gz')
# img = nib.load('haha.nii.gz').dataobj
# img = np.array(img)
# #print(img.shape)
# current = img[:,:,0]
# img2 = np.array(current, dtype=np.uint8)
# cv2.imshow('test2',img2)
# cv2.waitKey(0)












