import numpy as np
from typing import NamedTuple, Tuple

# type aliases
Vector3d = np.array

class Ray(NamedTuple):
    origin: Vector3d
    direction: Vector3d
    
    def is_advanced(self, t: float)-> Vector3d:
        vec = self.origin + t * self.direction
        return vec


class FieldOfView(NamedTuple):
    center: Vector3d
    width: Vector3d
    height: Vector3d
    
    def calc_point_at_uv(self, u: float, v: float)-> Vector3d:
        p = self.center + self.width * (u-.5) + self.height * (v-.5)
        return p


class Camera(NamedTuple):
    origin: Vector3d
    fov: FieldOfView
    
    @staticmethod
    def create(
            lookfrom: Vector3d,
            lookat: Vector3d,
            vup: Vector3d,
            width: int,
            height: int)-> 'Camera':
        unit_w = lookat - lookfrom
        unit_w /= np.linalg.norm(unit_w)
        unit_u = np.cross(unit_w, vup)
        unit_u /= np.linalg.norm(unit_u)
        unit_v = np.cross(unit_w, unit_u)
        fov = FieldOfView(lookat, width * unit_u, height * unit_v)
        camera = Camera(lookfrom, fov)
        return camera
    
    def calc_ray_from_uv(self, u: float, v: float)-> Ray:
        dir = self.fov.calc_point_at_uv(u, v) - self.origin
        dir /= np.linalg.norm(dir)
        ray = Ray(self.origin, dir)
        return ray
