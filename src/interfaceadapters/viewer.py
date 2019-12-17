import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class Viewer:
    @staticmethod
    def show(image: Image)->None:
        plt.imshow(np.array(image))
