import numpy as np
from typing import NamedTuple, Tuple

# type aliases
Vector3d = np.array
RGB_0_1 = Tuple[float, float, float]
RGB_0_255 = Tuple[int, int, int]

class Ray(NamedTuple):
    origin: Vector3d
    direction: Vector3d
    
    def is_advanced(self, t: float)-> Vector3d:
        vec = self.origin + t * self.direction
        return vec


class Color(NamedTuple):
    rgb: RGB_0_1

    max_uint8 = 255
    
    @staticmethod
    def create_by_y(ray: Ray)-> 'Color':
        dest = ray.is_advanced(1.)
        orig = ray.is_advanced(0.)
        dire = dest - orig
        t = np.clip(dire[1]*2, 0., 1.)
        top = np.array([0.5, 0.7, 1.])
        bottom = np.array([1.]*3)
        temp = (1-t) * top + t * bottom
        color = Color(tuple(temp))
        return color
    
    @staticmethod
    def create_by_point(p: Vector3d)-> 'Color':
        temp = p[:]
        temp /= np.linalg.norm(temp)
        temp = (temp + 1) / 2
        color = Color(tuple(temp))
        return color
    
    @staticmethod
    def create_red()-> 'Color':
        color = Color((1., 0., 0.))
        return color
    
    def to_uint8(self)-> RGB_0_255:
        ret = []
        for c in self.rgb:
            f = round(c*self.max_uint8)
            i = int(f)
            ret.append(i)
        return tuple(ret)


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
