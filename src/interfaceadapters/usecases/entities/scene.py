import numpy as np
from PIL import Image
from typing import List, NamedTuple, Tuple, Union
from . import Object3ds
from . import Camera, PositionAndDirection

# type aliases
RGB_0_1 = Tuple[float, float, float]
RGB_0_255 = Tuple[int, int, int]
MatrixX2d = np.array
MatrixX3d = np.array
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
    def create_by_y(ray: PositionAndDirection)-> 'Color':
        dire = ray.get_direction()
        t = np.clip(dire[1]*2, 0., 1.)
        top = np.array([0.5, 0.7, 1.])
        bottom = np.array([1.]*3)
        temp = (1-t) * top + t * bottom
        color = Color(tuple(temp))
        return color
    
    @staticmethod
    def create_by_normal_vector(n: MatrixX3d)-> List['Color']:
        temp = (n + 1) / 2
        colors = [Color(tuple(color)) for color in temp]
        return colors
    
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
    
    def calc_color_at_uv(self, uv: MatrixX2d)-> Color:
        ray = self.camera.calc_ray_from_uv(uv)
        hit = self.object3ds.calc_hit(ray)
        color = Color.create_by_y(ray)
        if hit is not None:
            colors = Color.create_by_normal_vector(hit.get_direction())
            colors += [color]*(self.num_samples-len(colors))
            color = Color.calc_mean(colors)
        return color
    
    def render(self)-> None:
        nx = self.image.width
        ny = self.image.height
        nxy = np.array([nx, ny])
        for j in range(ny):
            for i in range(nx):
                ij = np.array([i, j])
                uv = (ij + np.random.rand(self.num_samples, 2)) / nxy
                color = self.calc_color_at_uv(uv)
                self.image.putpixel((i, j), color.to_uint8())
