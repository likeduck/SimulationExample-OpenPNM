import openpnm as op
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

"""
openpnm==3.1.1
numpy==1.23.4
matplotlib==3.6.1
"""

# 输出设置
matplotlib.use('Tkagg')
np.random.seed(10)
plt.rcParams['figure.figsize'] = (8, 8)
np.set_printoptions(precision=5)
# np.set_printoptions(threshold=np.inf)

# 创建一个Z=1的平面
pn = op.network.Demo(shape=[40, 40, 1], spacing=1)
pn.add_model(propname='pore.diameter', model=op.models.geometry.pore_size.random, num_range=[0.01, 0.2])
# print(pn)

# 网络可视化
ax = op.visualization.plot_coordinates(network=pn, size_by=pn['pore.diameter'], color_by=pn['pore.diameter'], markersize=100)
ax = op.visualization.plot_connections(network=pn, ax=ax, c='k', alpha=0.6)
plt.title('Network 40*40')
plt.tight_layout()
plt.axis('off')
plt.show()

# 设置流体
air = op.phase.Air(network=pn)
air['pore.contact_angle'] = 120
air['pore.surface_tension'] = 0.072
f = op.models.physics.capillary_pressure.washburn
air.add_model(propname='throat.entry_pressure',
              model=f, 
              surface_tension='throat.surface_tension',
              contact_angle='throat.contact_angle',
              diameter='throat.diameter',)

# 设置算法
drn = op.algorithms.Drainage(network=pn, phase=air)
drn.set_inlet_BC(pores=pn.pores('left'))
drn.run()
# print(drn)

# 侵入路径可视化
inv_pattern = drn['throat.invasion_pressure'] < 0.7

ax = op.visualization.plot_coordinates(network=pn, pores=pn.pores('left'), c='r', s=50)
ax = op.visualization.plot_coordinates(network=pn, pores=pn.pores('left', mode='not'), c='grey', ax=ax)
op.visualization.plot_connections(network=pn, throats=inv_pattern, ax=ax)
plt.title('Invision Process')
plt.tight_layout()
plt.axis('off')
plt.show()

# 毛管力曲线
data = drn.pc_curve()
plt.plot(data.pc, data.snwp, 'k-.', linewidth=2)
plt.xlabel('Capillary_Pressure/Pa')
plt.ylabel('Non-Wetting_Phase_Saturation')
plt.title('Pc-Saturation')
plt.tight_layout()
plt.show()

# 考虑孔隙捕集
drn.set_outlet_BC(pores=pn.pores('right'), mode='overwrite')
drn.apply_trapping()
data2 = drn.pc_curve()
ax = op.visualization.plot_coordinates(network=pn, pores=pn.pores('left'), c='r', s=50)
ax = op.visualization.plot_coordinates(network=pn, pores=pn.pores('left', mode='not'), c='grey', ax=ax)
op.visualization.plot_connections(network=pn, throats=inv_pattern, ax=ax)
plt.title('With-trapping')
plt.tight_layout()
plt.axis('off')
plt.show()

# 毛管力曲线
plt.plot(data.pc, data.snwp, 'b-.', linewidth=2, label='without trapping')
plt.plot(data2.pc, data2.snwp, 'r-.', linewidth=2, label='with trapping')
plt.xlabel('Capillary_Pressure/Pa')
plt.ylabel('Non-Wetting_Phase_Saturation')
plt.legend()
plt.title('Pc-Saturation')
plt.tight_layout()
plt.show()

# 设置StokesFlow显示压力变化
phase = op.phase.Phase(network=pn, name='oil')
phase['pore.viscosity'] = 1
phase.add_model_collection(op.models.collections.physics.basic)
phase.regenerate_models()

inlet = pn.pores('left')
outlet = pn.pores('right')
flow = op.algorithms.StokesFlow(network=pn, phase=phase)
flow.set_value_BC(pores=inlet, values=1)
flow.set_value_BC(pores=outlet, values=0)
flow.run()
phase.update(flow.soln)
print(phase['pore.pressure'])

# 压力可视化
ax = op.visualization.plot_connections(pn, alpha=0.5)
ax = op.visualization.plot_coordinates(pn, ax=ax, color_by=phase['pore.pressure'], size_by=pn['pore.diameter'], markersize=100)
plt.title('Pressure')
plt.tight_layout()
plt.axis('off')
plt.show()

# 压力曲线
p = phase['pore.pressure'].reshape((40, 40)).mean(axis=1)
plt.plot(range(0, 40), p, 'k-.')
plt.title('Pressure-X')
plt.xlabel('X/2.5cm')
plt.ylabel('Pressure/Pa')
plt.tight_layout()
plt.show()

# 预测渗透率
Q = flow.rate(pores=inlet, mode='group')[0]
A = 40 # 2D厚度为 1
L = 40
K = Q * L / A
print(f'The value of K is: {K*1000:.2f} mD')
































