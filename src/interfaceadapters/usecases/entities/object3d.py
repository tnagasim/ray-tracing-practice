import math
import numpy as np
from typing import List, NamedTuple, Tuple, Union
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
        hits = list(filter(lambda hit: hit.get_position().size > 0 , hits))
        if hits == []:
            return None
        ray_p = ray.get_position()
        def func(hit: PositionAndDirection):
            d = np.linalg.norm(hit.get_position() - ray_p, axis=1)
            ave = sum(d) / len(d)
            return ave
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
        b_is_non_negative = b >= 0.
        c = np.dot(o_to_c, o_to_c) - self.radius * self.radius
        d = b * b - c
        d_is_zero = np.isclose(d, 0., rtol=1.e-9)
        d[d_is_zero] = 0.
        d_is_negative = d < 0.
        d_is_non_negative = d >= 0.
        d[d_is_negative] = 0.
        t = b - np.sqrt(d)
        position = ray.is_advanced(t)
        position = position[b_is_non_negative + d_is_non_negative]
        direction = position - self.center
        norm = np.linalg.norm(direction, axis=1)
        reciprocal = np.reciprocal(norm)
        reciprocal = reciprocal.reshape((reciprocal.size, 1))
        direction *= reciprocal
        hit = PositionAndDirection(position, direction)
        return hit
