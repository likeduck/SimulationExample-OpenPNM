import numpy as np
import porespy as ps
import matplotlib
import matplotlib.pyplot as plt 
import openpnm as op
import scipy.ndimage as spim
from skimage import io
from porespy.filters import find_peaks, trim_saddle_points, trim_nearby_peaks
from porespy.tools import randomize_colors
from skimage.segmentation import watershed

matplotlib.use('Tkagg')
plt.rcParams.update({'font.size': 16})
plt.rcParams['font.sans-serif'] = ['times new roman']
ps.settings.tqdm['disable'] = True
np.random.seed(10)

ws = op.Workspace()
ws.settings['loglevel'] = 50
ws.clear()


# read 2D digital core
path = 'Your image path'
fname = 'your image name with suffix .tif'
im = io.imread(path + fname, as_gray=True)

voxel_size = 1e-6  # meter/pixel

# porosity
im = im < 1
imtype = im.view()
im = np.array(im, dtype=bool)
im = ~im 
im = im.T
porosity = ps.metrics.porosity(im)
porosity_excel = [porosity]

# profile porosity
voxel_size = voxel_size
x_profile = ps.metrics.porosity_profile(im, 0)
y_profile = ps.metrics.porosity_profile(im, 1)
# z_profile = ps.metrics.porosity_profile(im, 2)
plt.figure(figsize=[10, 10])
plt.plot(np.linspace(0, im.shape[0]*voxel_size, im.shape[0]), x_profile, 'b-', label='yz-plane', alpha=0.7)
plt.plot(np.linspace(0, im.shape[1]*voxel_size, im.shape[1]), y_profile, 'r-', label='xz-plane', alpha=0.7)
# plt.plot(np.linspace(0, im.shape[2]*voxel_size, im.shape[2]), z_profile, 'g-', label='xy-plane', alpha=0.5)
plt.ylabel('Porosity of slice')
plt.xlabel('Position of slice along given axis')
plt.legend()
plt.show()

voxel_size = voxel_size
boundary_faces = ['top', 'bottom', 'left', 'right', 'front', 'back']
marching_cubes_area = False
r_max = 5
sigma = 0.35
regions = ps.filters.snow_partitioning(im=im, r_max=r_max, sigma=sigma)

regions_temp = regions.regions*regions.im

props = ps.metrics.regionprops_3D(regions_temp)
r = props[0]

df = ps.metrics.props_to_DataFrame(props)
# df.iloc[0]

sph = ps.metrics.prop_to_image(regionprops=props, shape=im.shape, prop='inscribed_sphere')

sph = ps.metrics.prop_to_image(regionprops=props, shape=im.shape, prop='solidity')

sigma = 0.5
dt = spim.distance_transform_edt(input=im)
dt1 = spim.gaussian_filter(input=dt, sigma=sigma)
peaks = find_peaks(dt=dt)

peaks = trim_saddle_points(peaks=peaks, dt=dt1)
peaks = trim_nearby_peaks(peaks=peaks, dt=dt)
peaks, N = spim.label(peaks)

regions = watershed(image=-dt, markers=peaks, mask=dt > 0)
regions = randomize_colors(regions)

net = ps.networks.regions_to_network(regions*im, voxel_size=voxel_size)
pn = op.io.network_from_porespy(net)

pn.add_model_collection(op.models.collections.geometry.spheres_and_cylinders)
pn.regenerate_models()


fig, ax = plt.subplots(figsize=[10, 10])
op.visualization.plot_connections(pn, c='k', linewidth=0.5, ax=ax)
op.visualization.plot_coordinates(pn, markersize=400, size_by=pn['pore.inscribed_diameter'], c='white', edgecolor='k', ax=ax)
max_x = pn['pore.coords'][:, 0].max()
max_y = pn['pore.coords'][:, 1].max()
x = [[0, max_x], [0, 0], [0, 0], [0, max_x], [0, 0], [max_x, max_x], [max_x, max_x], [0, 0], [0, max_x], [max_x, 0], [max_x, max_x], [max_x, max_x]]
y = [[0, 0], [0, max_y], [0, 0], [0, 0], [0, max_y], [0, max_y], [0, 0], [max_y, max_y], [max_y, max_y], [max_y, max_y], [max_y, 0], [max_y, max_y]]
for i in range(len(x)):
    plt.plot(x[i], y[i], color='k')
plt.axis('off')
ax.axis("off")
# fig.savefig(path+"PNM.png", bbox_extra_artists=None, bbox_inches='tight', dpi=300)
plt.show()
