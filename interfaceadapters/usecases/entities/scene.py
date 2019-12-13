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
    
    def calc_hit_point(self, ray: Ray)-> Vector3d_or_None:
        hit_points = map(lambda obj: obj.calc_hit_point(ray), self.objs)
        hit_points = list(filter(lambda point: point is not None, hit_points))
        if hit_points == []:
            return None
        def func(point: Vector3d):
            return np.dot(point, ray.direction)
        nearest_point = min(hit_points, key=func)
        return nearest_point
    
    def render(self):
        nx = self.image.width
        ny = self.image.height
        for j in range(ny):
            for i in range(nx):
                u = (i + random.random()) / nx
                v = (j + random.random()) / ny
                ray = self.camera.calc_ray_from_uv(u, v)
                hit_point = self.calc_hit_point(ray)
                if hit_point is None:
                    color = Color.create_by_y(ray)
                else:
                    color = Color.create_by_point(hit_point)
                self.image.putpixel((i, j), color.to_uint8())
