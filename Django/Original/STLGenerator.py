import nibabel as nib
import scipy.ndimage as ndimg
import numpy as np
import Original
from Original import Surface
import time
from stl import mesh
import os

#生成表面数据
def build_surf3d(imgs, ds, level, spacing, step=1, c=(1,0,0)):
	"""
	ds is the down sampling rate
	"""
	from skimage.measure import marching_cubes_lewiner
	vts, fs, ns, cs =  marching_cubes_lewiner(imgs[::ds,::ds,::ds], level, spacing, step_size=step)
	vts *= ds
	cs = (np.ones((len(vts), 3))*c).astype(np.float32)
	return vts, fs, ns, cs


#STL模型文件生成函数：SourcePath：读取的路径，DestPath：保存的文件夹路径
def GenSTL(SourcePath, DestPath):
    nii = nib.load(SourcePath)
    imgs = nii.get_data()  # imgs.shape = (x,y,z)
    print(imgs.shape);
    zoom = nii.header.get_zooms()# 确定标架
    # 高斯平滑
    organ_1 = ndimg.gaussian_filter(np.float32(imgs == 1), 1)
    organ_2 = ndimg.gaussian_filter(np.float32(imgs == 2), 1)
    organ_3 = ndimg.gaussian_filter(np.float32(imgs == 3), 1)

    # vts, fs, ns, cs are nodes，surface，normal vector, and color respectively
    vts, fs, ns, vs = build_surf3d(organ_1, 1, 0.5, zoom)
    vts2, fs2, ns2, vs2 = build_surf3d(organ_2, 1, 0.5, zoom)
    vts3, fs3, ns3, vs3 = build_surf3d(organ_3, 1, 0.5, zoom)


    loader = Original.Loader();
    loader.add_surf('1', vts, fs, ns, (1, 0, 0))  # 神经根
    objs = loader.objs.values()
    vers = [i.vts[i.ids] for i in objs if isinstance(i, Surface)]
    vers = np.vstack(vers)
    model = mesh.Mesh(np.zeros(vers.shape[0], dtype=mesh.Mesh.dtype))
    model.vectors = vers
    model.save(os.path.join(DestPath,'SJG.stl'))
    print("成功生成神经根")

    loader = Original.Loader();
    loader.add_surf('2', vts2, fs2, ns2, (0, 1, 0))  # 椎间盘
    objs = loader.objs.values()
    vers = [i.vts[i.ids] for i in objs if isinstance(i, Surface)]
    vers = np.vstack(vers)
    model = mesh.Mesh(np.zeros(vers.shape[0], dtype=mesh.Mesh.dtype))
    model.vectors = vers
    model.save(os.path.join(DestPath,'ZJP.stl'))
    print("成功生成椎间盘")

    loader = Original.Loader();
    loader.add_surf('3', vts3, fs3, ns3, (0, 0, 1))  # 硬膜囊
    objs = loader.objs.values()
    vers = [i.vts[i.ids] for i in objs if isinstance(i, Surface)]
    vers = np.vstack(vers)
    model = mesh.Mesh(np.zeros(vers.shape[0], dtype=mesh.Mesh.dtype))
    model.vectors = vers
    model.save(os.path.join(DestPath,'YMN.stl'))
    print("成功生成硬膜囊")



# start = time.time()
# GenSTL('spine1_0.nii.gz','/home/sxchongya/original_file/aaa')
# end = time.time()
# duration = end-start
# print('总耗时：'+ str(duration));






