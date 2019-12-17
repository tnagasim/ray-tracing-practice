# %%
import cloudpickle
from PIL import Image
from typing import Union

union = Union[Image.Image]

# %%
class DataAccess:
    @staticmethod
    def save(obj: union, file_path: str)-> None:
        if type(obj) is Image:
            return DataAccess.__save_image(obj, file_path)
        DataAccess.__save_other(obj, file_path)

    @staticmethod
    def __save_image(image: Image, file_path: str)-> None:
        image.save(file_path)
    
    @staticmethod
    def __save_other(obj: union, file_path: str)-> None:
        with open(file_path, 'wb') as f:
            f.write(cloudpickle.dump(obj))
