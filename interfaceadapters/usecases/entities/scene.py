import numpy as np
from PIL import Image
import random
from typing import Tuple, Union
from .object3d import Object3d, Object3ds
from .rayt import Camera, Color, Ray

# type aliases
Vector3d = np.array
Vector3d_or_None = Union[Vector3d, None]

class Scene:
    def __init__(self, camera: Camera, image: Image, object3ds: Object3ds)-> None:
        self.camera = camera
        self.image = image
        self.object3ds = object3ds
    
    def render(self)-> None:
        nx = self.image.width
        ny = self.image.height
        for j in range(ny):
            for i in range(nx):
                u = (i + random.random()) / nx
                v = (j + random.random()) / ny
                ray = self.camera.calc_ray_from_uv(u, v)
                hit_point = self.object3ds.calc_hit_point(ray)
                if hit_point is None:
                    color = Color.create_by_y(ray)
                else:
                    color = Color.create_by_point(hit_point)
                self.image.putpixel((i, j), color.to_uint8())
