import openpnm as op 
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 设置输出格式
matplotlib.use('TkAgg')
plt.rcParams['figure.figsize'] = (8, 8)
np.set_printoptions(precision=5)

ws = op.Workspace()
ws.clear()

import bz2
import pickle
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data
fname = 'PNM'
pn = decompress_pickle(fname + '.pbz2')
print(pn)

# 设置流体
air = op.phase.Air(network=pn)
air['pore.viscosity'] = 1.0  # Pa.s
air['throat.hydraulic_conductance'] = 1  # 水力传导系数 = kρg/μ
phy = op.models.collections.physics.basic
air.add_model_collection(phy)
air.regenerate_models()
print(air)
# print(air.keys())
# print(air.items())

# 添加算法 - Stokes flow
inlet = pn.pores('inlets')
outlet = pn.pores('outlets')
flow = op.algorithms.StokesFlow(network=pn, phase=air)
flow.set_value_BC(pores=inlet, values=1)
flow.set_value_BC(pores=outlet, values=0)
flow.run()
air.update(flow.soln)

# 压力变化图
ax = op.visualization.plot_connections(pn, alpha=0.6)
ax = op.visualization.plot_coordinates(pn, ax=ax, color_by=air['pore.pressure'], size_by=pn['pore.diameter'], edgecolor='k', markersize=300)
plt.axis('off')
plt.title('Pressure')
plt.tight_layout()
plt.show()

# 预测绝对渗透率 Kabs = QμL/(A·ΔP)
Q = flow.rate(pores=inlet, mode='group')[0]
# A = op.topotools.get_domain_area(pn, inlets=inlet, outlets=outlet)
# L = op.topotools.get_domain_length(pn, inlets=inlet, outlets=outlet)
L = 10
A = 100
K = Q * L / A
print(f'The value of K is: {K*1000:.2f} mD')






































