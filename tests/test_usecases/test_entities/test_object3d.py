# %%
import sys
sys.path.append('src/')
import math
import numpy as np
import pytest
from interfaceadapters.usecases.entities import Ray
from interfaceadapters.usecases.entities import Sphere

@pytest.fixture()
def sphere():
    center = np.array([0., 0., 0.])
    radius = 1.
    sphere1 = Sphere(center, radius)
    yield sphere1

@pytest.mark.parametrize(
    "origin, direction, expected", [
        ([0., 0., -2.], [0., 0., 1.], [0., 0., -1.]),
        ([0., 0., -2.], [0., 1/np.sqrt(2), 1/np.sqrt(2)], None),
        ([0., 0., -2.], [0., .5, np.sqrt(3)/2], [0., np.sqrt(3)/2, -.5]),
        ([1., 0., -2.], [0., 0., 1.], [1., 0., 0.]),
        ([1., 0., -2.], [-.8, 0., .6], [-3/5, 0., -4/5])
    ]
)

def test_calc_hit_point(sphere, origin, direction, expected):
    origin = np.array(origin)
    direction = np.array(direction)
    ray = Ray(origin, direction)
    point = sphere.calc_hit_point(ray)
    if expected is None:
        assert point is None
    else:
        for p, e in zip(point, expected):
            assert math.isclose(p, e)

# %%
center = np.array([0., 0., 0.])
radius = 1.
sphere1 = Sphere(center, radius)
test_calc_hit_point(sphere1, [1., 0., -2.], [-.8, 0., .6], [-3/5, 0., -4/5])
