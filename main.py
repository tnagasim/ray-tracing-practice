# %%
from IPython import get_ipython
if get_ipython():
    get_ipython().run_line_magic('reload_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')

# %%
import numpy as np
from PIL import Image
from interfaceadapters import Viewer
from interfaceadapters.usecases.entities import Camera, Color, FieldOfView
from interfaceadapters.usecases.entities import Sphere

# %%
nx = 200
ny = 100
image = Image.new('RGB', (nx, ny))

# %%
x = np.array([4., 0., 0.])
y = np.array([0., 2., 0.])
z = np.array([0., 0., 1.])
o = np.array([0., 0., 0.])
camera = Camera(o, FieldOfView(z, x, y))

# %%
center = np.array([0., 0., 2])
radius = 1.
sphere = Sphere(center, radius)

# %%
for j in range(ny):
    for i in range(nx):
        u = i / nx
        v = j / ny
        ray = camera.calc_ray_from_uv(u, v)
        p = sphere.hit(ray)
        if p is None:
            color = Color.create_by_y(ray)
        else:
            color = Color.create_by_point(p)
        image.putpixel((i, j), color.to_uint8())

# %%
Viewer.show(image)

# %%
