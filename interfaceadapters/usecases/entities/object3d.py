import numpy as np
from typing import Union
from .rayt import Ray, Color

# type aliases
Vector3d = np.array
Vector3d_or_None = Union[Vector3d, None]

class Sphere:
    def __init__(self, center: np.array, radius: float):
        self.center_ = center
        self.radius_ = radius
    
    def hit(self, ray: Ray)-> Vector3d_or_None:
        ray_o = ray.is_advanced(0.)
        ray_d = ray.is_advanced(1.) - ray_o
        o_to_c = self.center_ - ray_o
        b = np.dot(ray_d, o_to_c)
        c = np.dot(o_to_c, o_to_c) - self.radius_ * self.radius_
        d = b * b - c
        if d < 0.:
            return None
        t = b - np.sqrt(d)
        p = ray.is_advanced(t)
        return p
