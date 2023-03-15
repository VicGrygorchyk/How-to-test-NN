from glob import glob
from typing import List
from dataclasses import dataclass
from collections import namedtuple
import base64


CategoryTuple = namedtuple('categoryTuple', 'Cat Dog')
categories = CategoryTuple(Cat=0, Dog=1)


@dataclass
class DatasetItem:
    source: str
    image: str
    category: categories


def decode_img_to_base64(image_path):
    with open(image_path, "rb") as f:
        im_b64 = base64.b64encode(f.read())
        return im_b64.decode('utf-8')


def load_cats(path) -> List[DatasetItem]:
    results = []
    for img_file in glob(f'{path}/*'):
        img = decode_img_to_base64(img_file)
        results.append(DatasetItem(img_file, img, 0))
    return results


def load_dogs(path) -> List[DatasetItem]:
    results = []
    for img_file in glob(f'{path}/*'):
        img = decode_img_to_base64(img_file)
        results.append(DatasetItem(img_file, img, 1))
    return results
