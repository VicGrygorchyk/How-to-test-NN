import asyncio
import json
from typing import TYPE_CHECKING, List

import aiohttp

if TYPE_CHECKING:
    from .dataset_util import DatasetItem


HEADERS = {
  'Content-Type': 'application/json'
}


class ApiClient:

    def __init__(self, solution_url: str):
        self.lock = asyncio.Lock()
        self.saved = []
        self.result_categories = []
        self.errors = []
        self.solution_url = solution_url

    async def run_post(self, session: 'aiohttp.ClientSession', image: 'DatasetItem'):
        data = {
            "src": image.image
        }

        async with session.post(self.solution_url, data=json.dumps(data)) as resp:
            if resp.status == 200:
                result = await resp.json()
                async with self.lock:
                    expected = True if image.category == 0 else False
                    self.result_categories.append(result['is_cat'] == expected)
                    self.saved.append(
                        {
                            'source': image.source,
                            'is_correct_prediction': result['is_cat'] == expected,
                            'predicted_category': 0 if result['is_cat'] else 1,
                            'expected_category': image.category,
                        }
                    )
            else:
                self.errors.append(f'Request has finished with status code {resp.status}')

    async def get_results(self, dataset: List['DatasetItem']):
        conn = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=conn, headers=HEADERS) as session:
            results = await asyncio.gather(
                *[self.run_post(session, img) for img in dataset], return_exceptions=True
            )
            return results
