from typing import List


def get_accuracy(results: List[bool]):
    length = len(results)
    trues = results.count(True)
    return trues * 100 / length
