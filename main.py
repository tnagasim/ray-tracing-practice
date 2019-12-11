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
from interfaceadapters.usecases.entities import Scene
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
objs = (sphere, )

# %%
scene = Scene(camera, image, objs)
scene.render()

# %%
Viewer.show(image)

# %%
