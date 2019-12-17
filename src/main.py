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
from interfaceadapters.usecases.entities import Camera, FieldOfView
from interfaceadapters.usecases.entities import Scene
from interfaceadapters.usecases.entities import Object3ds, Sphere

# %%
nx = 200
ny = 100
image = Image.new('RGB', (nx, ny))

# %%
x = np.array([4., 0., 0.])
y = np.array([0., 2., 0.])
z = np.array([0., 0., .5])
o = np.array([0., 1., 0.])
camera = Camera(o, FieldOfView(z, x, y))

# %%
center1 = np.array([0., 0., 1])
radius1 = .5
sphere1 = Sphere(center1, radius1)

# %%
center2 = np.array([0., 1.5, 1])
radius2 = 1.
sphere2 = Sphere(center2, radius2)

# %%
objs = Object3ds((sphere2, ))

# %%
scene = Scene(camera, image, objs)
scene.render()

# %%
Viewer.show(image)

# %%
