import math
import numpy as np
from typing import NamedTuple, Tuple, Union
from . import PositionAndDirection

# type aliases
Vector3d = np.array
PositionAndDirection_or_None = Union[PositionAndDirection, None]

class Object3d:
    pass


# type aliases
Objs = Tuple[Object3d, ...]

class Object3ds:
    def __init__(self, objs: Objs)-> None:
        self.objs = objs
    
    def calc_hit(self, ray: PositionAndDirection)-> PositionAndDirection_or_None:
        hits = map(lambda obj: obj.calc_hit(ray), self.objs)
        hits = list(filter(lambda hit: hit is not None, hits))
        if hits == []:
            return None
        ray_d = ray.get_direction()
        def func(hit: PositionAndDirection):
            return np.dot(hit.get_position(), ray_d)
        hit = min(hits, key=func)
        return hit


class Sphere(NamedTuple, Object3d):
    center: Vector3d
    radius: float
    
    def calc_hit(self, ray: PositionAndDirection)-> PositionAndDirection_or_None:
        ray_p = ray.get_position()
        ray_d = ray.get_direction()
        o_to_c = self.center - ray_p
        b = np.dot(ray_d, o_to_c)
        if b < 0.:
            return None
        c = np.dot(o_to_c, o_to_c) - self.radius * self.radius
        d = b * b - c
        if math.isclose(d, 0., abs_tol=1.e-9):
            d = 0.
        if d < 0.:
            return None
        t = b - np.sqrt(d)
        p = ray.is_advanced(t)
        d = p - self.center
        d /= np.linalg.norm(d)
        hit = PositionAndDirection(p, d)
        return hit
