import numpy as np
from PIL import Image
from typing import List, NamedTuple, Tuple, Union
from . import Object3ds
from . import Camera, PositionAndDirection

# type aliases
RGB_0_1 = Tuple[float, float, float]
RGB_0_255 = Tuple[int, int, int]
Vector2d = np.array
Vector3d = np.array
Vector3d_or_None = Union[Vector3d, None]

def random_in_unit_sphere():
    vec = np.random.rand(3) * 2 - np.ones(3)
    while np.linalg.norm(vec) > 1.:
        vec = np.random.rand(3) * 2 - np.ones(3)
    return vec


class Color(NamedTuple):
    rgb: RGB_0_1

    max_uint8 = 255
    
    def __mul__(self, v: float)-> 'Color':
        rgb = np.array(self.rgb) * v
        return Color(rgb)
    
    @staticmethod
    def calc_mean(colors: List['Color'])-> 'Color':
        total = sum(np.array(color.rgb) for color in colors)
        mean = total / len(colors)
        color = Color(tuple(mean))
        return color

    @staticmethod
    def create_by_y(ray: PositionAndDirection)-> 'Color':
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
    def create_by_normal_vector(n: Vector3d)-> 'Color':
        temp = (n + 1) / 2
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
    
    def calc_color_at_uv(self, uv: Vector2d)-> Color:
        ray = self.camera.calc_ray_from_uv(uv)
        return self.calc_color_by_ray(ray)
    
    def calc_color_by_ray(self, ray: PositionAndDirection)->Color:
        hit = self.object3ds.calc_hit(ray)
        if hit is None:
            color = Color.create_by_y(ray)
        else:
            position = hit.get_position()
            direction = hit.get_direction() + random_in_unit_sphere()
            direction /= np.linalg.norm(direction)
            ray = PositionAndDirection(position, direction)
            color = self.calc_color_by_ray(ray) * 0.5
        return color
    
    def render(self)-> None:
        nx = self.image.width
        ny = self.image.height
        nxy = np.array([nx, ny])
        for j in range(ny):
            for i in range(nx):
                colors = []
                ij = np.array([i, j])
                for _ in range(self.num_samples):
                    uv = (ij + np.random.rand(2)) / nxy
                    color = self.calc_color_at_uv(uv)
                    colors.append(color)
                color = Color.calc_mean(colors)
                self.image.putpixel((i, j), color.to_uint8())
