import openpnm as op 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np

# 设置输出格式
matplotlib.use('TkAgg')
plt.rcParams['figure.figsize'] = (8, 8)
np.set_printoptions(precision=5)
np.random.seed(10)

ws = op.Workspace()
ws.clear()

# # 测试：生成岩心
# pn = op.network.Cubic(shape=[15, 15, 15], spacing=1)
# pn.add_model_collection(op.models.collections.geometry.spheres_and_cylinders)
# pn.regenerate_models()
# print(pn.items())

# 导入PNM
path = 'D:\simulation\PNM\\200_200_200_voxels'
prefix='network'
project = op.io.network_from_statoil(path=path, prefix=prefix)
pn = project.network

pn['throat.diameter'] = pn['throat.radius']*2
pn['pore.diameter'] = pn['pore.radius']*2
pn['pore.left'] = pn['pore.inlets']
pn['pore.right'] = pn['pore.outlets']

del pn['throat.conduit_lengths.pore1']
del pn['throat.conduit_lengths.pore2']
del pn['throat.conduit_lengths.throat']
del pn['pore.radius']
del pn['throat.radius']
del pn['pore.clay_volume']
del pn['throat.clay_volume']

# print(pn.keys(), pn.items())
print(pn)

# # PNM几何特征
# fig, ax = plt.subplots()
# ax = plt.hist(pn['throat.diameter'], edgecolor='k', density=True, alpha=0.6, label='Throat')
# ax = plt.hist(pn['pore.diameter'], edgecolor='k', density=True, alpha=0.6, label='Pore')
# plt.title('Pore-Throat Distribution before trimming')
# plt.tight_layout()
# plt.legend()
# plt.show()

# # PNM可视化
# ax = op.visualization.plot_coordinates(network=pn, c='g', markersize=pn['pore.diameter']*5e+9, edgecolor='k', alpha=1)
# ax = op.visualization.plot_connections(network=pn, c='r', linewidth=pn['throat.diameter']*1e+8, alpha=0.4, ax=ax)
# plt.title('PNM before trimming')
# plt.axis('off')    # 不显示坐标系
# plt.tight_layout() # 图像完整显示
# plt.show()

# Check PNM health & Trim
pn.add_model(propname='pore.cluster_number',
             model=op.models.network.cluster_number)
pn.add_model(propname='pore.cluster_size',
             model=op.models.network.cluster_size)
print(pn)
print(pn['pore.cluster_number'])  # cluster_number相同则属于同一簇
print(pn['pore.cluster_size'])    # 查看main cluster
Ps = pn['pore.cluster_size'] < 4678
op.topotools.trim(network=pn, pores=Ps)

# PNM可视化
ax = op.visualization.plot_coordinates(network=pn, c='g', markersize=pn['pore.diameter']*5e+9, edgecolor='k', alpha=1)
ax = op.visualization.plot_connections(network=pn, c='r', linewidth=pn['throat.diameter']*1e+8, alpha=0.4, ax=ax)
plt.title('PNM after trimming')
plt.axis('off')
plt.tight_layout()
# plt.show()

# PNM几何特征
# 孔喉直径分布
fig, ax = plt.subplots()
ax = plt.hist(pn['throat.diameter'], edgecolor='k', density=True, alpha=0.8, label='Throat')
ax = plt.hist(pn['pore.diameter'], color='r', edgecolor='k', density=True, alpha=0.8, label='Pore')
plt.title('Diameter')
plt.tight_layout()
plt.legend()
# 形状因子分布
fig, ax = plt.subplots()
ax = plt.hist(pn['throat.shape_factor'], edgecolor='k', bins=30, density=True, alpha=0.8, label='Throat')
ax = plt.hist(pn['pore.shape_factor'], color='r', edgecolor='k', bins=30, density=True, alpha=0.8, label='Pore')
plt.title('Shape_factor')
plt.tight_layout()
plt.legend()
# 孔喉体积
fig, ax = plt.subplots()
ax = plt.hist(pn['throat.volume'], edgecolor='k', bins=15, density=True, alpha=0.8, label='Throat')
ax = plt.hist(pn['pore.volume'], color='r', edgecolor='k', bins=15, density=True, alpha=0.8, label='Pore')
plt.title('Volume')
plt.tight_layout()
plt.legend()
plt.show()

# 添加几何信息
geo = op.models.collections.geometry.spheres_and_cylinders
pn.add_model_collection(geo)
print(pn)

# 保存文件之后读取
import bz2
import pickle
def compressed_pickle(title, data):
    with bz2.BZ2File(title + '.pbz2', 'w') as f:
        pickle.dump(data, f)
compressed_pickle('PNM', pn)