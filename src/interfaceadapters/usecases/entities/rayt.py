import numpy as np
from typing import NamedTuple, Tuple

# type aliases
MatrixX2d = np.array
MatrixX3d = np.array
Vector3d = np.array
VectorXd = np.array

class PositionAndDirection(NamedTuple):
    position: Vector3d
    direction: MatrixX3d
    
    def get_direction(self)-> Vector3d:
        return self.direction
    
    def get_position(self)-> MatrixX3d:
        return self.position
    
    def is_advanced(self, t: VectorXd)-> MatrixX3d:
        temp = t.reshape((t.size, 1))
        vec = self.position + self.direction * temp
        return vec


class FieldOfView(NamedTuple):
    center: Vector3d
    width: Vector3d
    height: Vector3d
    
    def calc_point_at_uv(self, uv: MatrixX2d)-> MatrixX3d:
        wh = np.array([self.width, self.height])
        p = self.center + np.dot((uv-.5), wh)
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
    
    def calc_ray_from_uv(self, uv: MatrixX2d)-> PositionAndDirection:
        direction = self.fov.calc_point_at_uv(uv) - self.position
        size = direction.size
        direction = direction.reshape((size//3, 3))
        norm = np.linalg.norm(direction, axis=1)
        reciprocal = np.reciprocal(norm)
        reciprocal = reciprocal.reshape((reciprocal.size, 1))
        direction *= reciprocal
        ray = PositionAndDirection(self.position, direction)
        return ray
