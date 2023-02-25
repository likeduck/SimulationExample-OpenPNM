import imageio
import porespy as ps
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt


# 输出设置
plt.rcParams['figure.figsize'] = (8, 8)


# 2D图像序列合成3D

# 读取2D图像序列
seq = io.imread_collection('D:\simulation\PNM\\tif\\2D_Slice\*.tif')
print(seq)
# 显示2D图像
fig, ax = plt.subplots()
ax.imshow(seq[0])
plt.show()
# 合成3D图像
im3d = np.zeros([*seq[0].shape, len(seq)])
for i, im in enumerate(seq):
    im3d[..., i] = im
print("3D图像大小为:", im3d.shape)
# 显示3D图像
fig, ax = plt.subplots()
ax.imshow(ps.visualization.show_planes(im3d));
plt.show()

# 保存3D图像
imageio.volsave('3D.tif', np.array(im3d, dtype=np.int8))