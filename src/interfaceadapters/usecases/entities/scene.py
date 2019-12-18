import numpy as np
from PIL import Image
import random
from typing import List, NamedTuple, Tuple, Union
from . import Object3ds
from . import Camera, Ray

# type aliases
RGB_0_1 = Tuple[float, float, float]
RGB_0_255 = Tuple[int, int, int]
Vector3d = np.array
Vector3d_or_None = Union[Vector3d, None]


class Color(NamedTuple):
    rgb: RGB_0_1

    max_uint8 = 255
    
    @staticmethod
    def calc_mean(colors: List['Color'])-> 'Color':
        total = sum(np.array(color.rgb) for color in colors)
        mean = total / len(colors)
        color = Color(tuple(mean))
        return color

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


class Scene:
    num_samples = 100

    def __init__(self,
            camera: Camera,
            image: Image,
            object3ds: Object3ds)-> None:
        self.camera = camera
        self.image = image
        self.object3ds = object3ds
    
    def calc_color_at_uv(self, u: float, v: float)-> Color:
        ray = self.camera.calc_ray_from_uv(u, v)
        hit_point = self.object3ds.calc_hit_point(ray)
        if hit_point is None:
            color = Color.create_by_y(ray)
        else:
            color = Color.create_by_point(hit_point)
        return color
    
    def render(self)-> None:
        nx = self.image.width
        ny = self.image.height
        for j in range(ny):
            for i in range(nx):
                colors = []
                for _ in range(self.num_samples):
                    u = (i + random.random()) / nx
                    v = (j + random.random()) / ny
                    color = self.calc_color_at_uv(u, v)
                    colors.append(color)
                color = Color.calc_mean(colors)
                self.image.putpixel((i, j), color.to_uint8())
