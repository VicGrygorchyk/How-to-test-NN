import json
from typing import TYPE_CHECKING, List
import asyncio

from .utils import get_accuracy
from .api_client import ApiClient

if TYPE_CHECKING:
    from .dataset_util import DatasetItem


URL_SOLUTION = 'http://localhost:8007/classify_cat'
BASELINE_SCORE = 80


def test_baseline_accuracy_async(dataset: List['DatasetItem']):
    api_client_manager = ApiClient(URL_SOLUTION)

    async def get_tests_results():
        test_results = await api_client_manager.get_results(dataset)
        return test_results

    # run all POST requests
    asyncio.run(get_tests_results())
    assert not api_client_manager.errors, f'Expected not to have API errors, got {api_client_manager.errors}'

    # get accuracy
    categories_acc = get_accuracy(api_client_manager.result_categories)
    with open('./tests_results.json', 'w+', encoding='utf-8') as f:
        json.dump(api_client_manager.saved, f, indent=4, ensure_ascii=False)

    assert categories_acc >= BASELINE_SCORE, \
        f'Expected the classification accuracy to be >= than {BASELINE_SCORE}, ' \
        f'got classification={categories_acc}'
