# %%
from IPython import get_ipython
if get_ipython():
    get_ipython().run_line_magic('reload_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')

# %%
import sys
sys.path.append('src')
import numpy as np
from PIL import Image
from interfaceadapters import Viewer
from interfaceadapters.usecases.entities import Camera
from interfaceadapters.usecases.entities import Scene
from interfaceadapters.usecases.entities import Object3ds, Sphere

# %%
nx = 200
ny = 100
image = Image.new('RGB', (nx, ny))

# %%
lookfrom = np.array([0., 0., -1.])
lookat = np.array([0., 0., 0.])
vup = np.array([0., -1., 0.])
width = 4.
height = 2.
camera = Camera.create(lookfrom, lookat, vup, width, height)

# %%
center1 = np.array([0., 0., 0.])
radius1 = .5
sphere1 = Sphere(center1, radius1)

# %%
center2 = np.array([0., 10.5, 1])
radius2 = 10.
sphere2 = Sphere(center2, radius2)

# %%
objs = Object3ds((sphere1, sphere2, ))

# %%
scene = Scene(camera, image, objs)
scene.render()

# %%
Viewer.show(image)

# %%
