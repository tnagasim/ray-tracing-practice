import numpy as np
from typing import NamedTuple, Union
from .rayt import Ray, Color

# type aliases
Vector3d = np.array
Vector3d_or_None = Union[Vector3d, None]

class Object3d:
    def hit(self, ray: Ray)-> Vector3d_or_None:
        return None

class Sphere(NamedTuple, Object3d):
    center: Vector3d
    radius: float
    
    def calc_hit_point(self, ray: Ray)-> Vector3d_or_None:
        ray_o = ray.is_advanced(0.)
        ray_d = ray.is_advanced(1.) - ray_o
        o_to_c = self.center - ray_o
        b = np.dot(ray_d, o_to_c)
        c = np.dot(o_to_c, o_to_c) - self.radius * self.radius
        d = b * b - c
        if d < 0.:
            return None
        t = b - np.sqrt(d)
        p = ray.is_advanced(t)
        return p
