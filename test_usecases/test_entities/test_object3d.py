import sys
sys.path.append('../../')
import numpy as np
import pytest
from interfaceadapters.usecases.entities import Ray
from interfaceadapters.usecases.entities import Sphere

@pytest.fixture()
def sphere():
    center = np.array([0., 0., 2.])
    radius = 1.
    sphere1 = Sphere(center, radius)
    yield sphere1

def test_calc_hit_point(sphere):
    origin = np.array([0., 0., 0.])
    direction = np.array([0., 0., 1.])
    ray = Ray(origin, direction)
    point = sphere.calc_hit_point(ray)
    assert point is not None
    
    origin = np.array([0., 0., 0.])
    direction = np.array([0., 1., 1.])
    direction /= np.linalg.norm(direction)
    ray = Ray(origin, direction)
    point = sphere.calc_hit_point(ray)
    assert point is None
    
    origin = np.array([0., 0., 0.])
    direction = np.array([0., np.sqrt(3)/2, 3/2])
    direction /= np.linalg.norm(direction)
    ray = Ray(origin, direction)
    point = sphere.calc_hit_point(ray)
    assert point is not None
