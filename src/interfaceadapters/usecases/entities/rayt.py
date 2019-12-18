import numpy as np
from typing import NamedTuple, Tuple

# type aliases
Vector3d = np.array

class PositionAndDirection(NamedTuple):
    position: Vector3d
    direction: Vector3d
    
    def get_direction(self)-> Vector3d:
        return self.direction
    
    def get_position(self)-> Vector3d:
        return self.position
    
    def is_advanced(self, t: float)-> Vector3d:
        vec = self.position + t * self.direction
        return vec


class FieldOfView(NamedTuple):
    center: Vector3d
    width: Vector3d
    height: Vector3d
    
    def calc_point_at_uv(self, u: float, v: float)-> Vector3d:
        p = self.center + self.width * (u-.5) + self.height * (v-.5)
        return p


class Camera(NamedTuple):
    position: Vector3d
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
    
    def calc_ray_from_uv(self, u: float, v: float)-> PositionAndDirection:
        dir = self.fov.calc_point_at_uv(u, v) - self.position
        dir /= np.linalg.norm(dir)
        ray = PositionAndDirection(self.position, dir)
        return ray
