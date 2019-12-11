import numpy as np
from PIL import Image
import random
from typing import Tuple, Union
from .object3d import Object3d
from .rayt import Camera, Color, Ray

# type aliases
Objs = Tuple[Object3d, ...]
Vector3d = np.array
Vector3d_or_None = Union[Vector3d, None]

class Scene:
    def __init__(self, camera: Camera, image: Image, objs: Objs):
        self.camera = camera
        self.image = image
        self.objs = objs
    
    def calc_min_hit_point(self, ray: Ray)-> Vector3d_or_None:
        min_hit_point = None
        for obj in self.objs:
            hit_point = obj.calc_hit_point(ray)
            if (min_hit_point is None) or (np.dot(hit_point, ray) < np.dot(min_hit_point, ray)):
                min_hit_point = hit_point
        return min_hit_point
    
    def render(self):
        nx = self.image.width
        ny = self.image.height
        for j in range(ny):
            for i in range(nx):
                u = (i + random.random()) / nx
                v = (j + random.random()) / ny
                ray = self.camera.calc_ray_from_uv(u, v)
                min_hit_point = self.calc_min_hit_point(ray)
                if min_hit_point is None:
                    color = Color.create_by_y(ray)
                else:
                    color = Color.create_by_point(min_hit_point)
                self.image.putpixel((i, j), color.to_uint8())
