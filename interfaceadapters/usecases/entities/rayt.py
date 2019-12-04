import numpy as np
from typing import Tuple

# type aliases
Vector3d = np.array
RGB_0_1 = Tuple[float, float, float]
RGB_0_255 = Tuple[int, int, int]

class Ray:
    def __init__(self, origin: Vector3d, direction: Vector3d):
        self.origin_ = origin
        self.direction_ = direction / np.linalg.norm(direction)
    
    def is_advanced(self, t: float)-> Vector3d:
        vec = self.origin_ + t * self.direction_
        return vec


class Color:
    max_uint8 = 255
    
    def __init__(self, rgb: RGB_0_1):
        self.rgb_ = rgb
    
    @staticmethod
    def create_by_y(ray: Ray)-> 'Color':
        dest = ray.is_advanced(1.)
        orig = ray.is_advanced(0.)
        dire = dest - orig
        t = np.clip(dire[1]*2, 0., 1.)
        top = np.array([0.5, 0.7, 1.])
        bottom = np.array([1.]*3)
        temp = t * top + (1-t) * bottom
        color = Color(tuple(temp))
        return color
    
    @staticmethod
    def create_red()-> 'Color':
        color = Color((1., 0., 0.))
        return color
    
    def to_uint8(self)-> RGB_0_255:
        ret = []
        for c in self.rgb_:
            f = round(c*self.max_uint8)
            i = int(f)
            ret.append(i)
        return tuple(ret)


class FieldOfView:
    def __init__(self, center: Vector3d, width: Vector3d, height: Vector3d):
        self.center_ = center[:]
        self.width_ = width[:]
        self.height_ = height[:]
    
    def calc_point_at_uv(self, u: float, v: float)-> Vector3d:
        p = self.center_ + self.width_ * (u-.5) + self.height_ * (v-.5)
        return p


class Camera:
    def __init__(self, origin: Vector3d, fov: FieldOfView):
        self.origin_ = origin[:]
        self.fov_ = fov
    
    @staticmethod
    def create(
            lookfrom: Vector3d,
            lookat: Vector3d,
            vup: Vector3d,
            vfov: float,
            aspect: float)-> 'Camera':
        unit_w = lookat - lookfrom
        unit_w /= np.linalg.norm(unit_w)
        unit_u = np.cross(vup, unit_w)
        unit_u /= np.linalg.norm(unit_u)
        unit_v = np.cross(unit_w, unit_u)
        height = np.tan(np.deg2rad(vfov)/2) * 2
        width = aspect * height
        fov = FieldOfView(lookat, width * unit_u, height * unit_v)
        camera = Camera(lookfrom, fov)
        return camera
    
    def calc_ray_from_uv(self, u: float, v: float)-> Ray:
        ray = Ray(self.origin_, self.fov_.calc_point_at_uv(u, v))
        return ray
