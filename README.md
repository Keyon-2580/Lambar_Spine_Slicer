# Lambar_Spine_Slicer
腰椎影像智能分割可视化系统，采用Vue+Django框架，3DUNet算法自动分割nii医疗影像文件，并且可以在前端生成分割后的部位三维建模的模型。
## 框架
在pycharm中运行Djsngo文件即可


前端代码在Vue中修改，默认8888端口

## 下载
下载相关依赖库
- numpy 
- SimpleITK 
- nibabel 
- scipy 
- pytorch
## 训练
训练时将训练集和测试集的数据和标签文件名称存在txt文件中，dataset类中获取数据 ,在utils类中处理数据

处理操作：
- ct影像阈值截断
- 归一化
- 缩小分辨率
使用dice值评估分割的准确率

config文件中设置相关参数

设置训练的模型大小，每次在输入文件中截取该大小的部分进行训练。

可以加上attention机制提高准确率
## 三维建模
将nii转为stl模型文件展示椎间盘，神经根，类囊膜渲染在前端

## 引用
https://github.com/lee-zq/3DUNet-Pytorch
