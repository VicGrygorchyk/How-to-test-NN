import pytest

from .dataset_util import load_cats, load_dogs


CATS_PATH = '/Users/Viktor_Hryhorchuk/Projects/test_nn/assets/cats_test'
DOGS_path = '/Users/Viktor_Hryhorchuk/Projects/test_nn/assets/dogs_test'


@pytest.fixture(scope='session')
def dataset():
    cats = load_cats(CATS_PATH)
    dogs = load_dogs(DOGS_path)
    cats.extend(dogs)
    return cats
