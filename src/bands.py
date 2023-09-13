"""
CSAPX Lab 3: Battle of the Bands
Given a list of bands and the number of votes they recived, find the most mediocre band (i.e. the band with the median amount of votes)

$ python3 bands.py [slow|fast] input-file

Author: RIT CS
Author: Max Klot
"""

from dataclasses import dataclass
import sys  # argv
import time  # clock
import random  # random

#from typing import List  # List


def main() -> None:
    """
   The main function.
   :return: None
   """
    unsortedBands = load_bands((getFilename()))
    if getSlowOrFast() == 'slow':
        print("Search type: slow")
        print("Number of bands: #" + str(len(unsortedBands)))
        start = time.perf_counter()
        sortedBands = quick_sort(load_bands(getFilename()))
        slowStr = ("Most mediocre band: " + sortedBands[len(sortedBands) // 2].name + " with " + str(
            sortedBands[len(sortedBands) // 2].votes) + " votes")
        print("Elapsed time: # " + str(round((time.perf_counter() - start), 3)) + " seconds")
        print(slowStr)

    elif getSlowOrFast() == 'fast':
        print("Search type: fast")
        print("Number of bands: #" + str(len(unsortedBands)))
        start = time.perf_counter()
        medianBand = quick_select(unsortedBands, len(unsortedBands) // 2)
        fastStr = ("The most mediocre band is " + medianBand.name + " with " + str(medianBand.votes) + " votes.")
        print("Elapsed time: # " + str(round((time.perf_counter() - start), 3)) + " seconds")
        print(fastStr)
    else:
        print("Invalid/no search type defined")


def getFilename() -> str:
    """
   getFilename returns the first sys.argv element, the test file defined in the run configuration
   :return: first sys.argv element as a string
   """
    return sys.argv[2]


def getSlowOrFast() -> str:
    """
   getSlowOrFast returns first sys.argv argument, whether to run quicksort or quickselect algo
   :return:
   """
    return sys.argv[1]


def load_bands(filename: str) -> list:
    """
   loads the bands from filename into a list
   :param filename: filepath to load band names from
   :return: list of bands loaded from filepath
   """
    bands = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            splitted = line.split("\t")
            bands.append(Band(
                name=splitted[0],
                votes=int(splitted[1])))
    return bands


@dataclass
class Band:
    """
   name: name of band
   votes: number of votes for band
   """
    name: str
    votes: int


def _partitionQuickSort(data: list[Band], pivot: Band) \
        -> tuple[list[Band], list[Band], list[Band]]:
    """
   Three-way partition the data into smaller, equal and greater lists,
   in relationship to the pivot
   :param data: The data to be sorted (a list)
   :param pivot: The value to partition the data on
   :return: Three list: smaller, equal and greater
   """
    less, equal, greater = [], [], []
    for element in data:
        if element.votes < pivot.votes:
            less.append(element)
        elif element.votes > pivot.votes:
            greater.append(element)
        else:
            equal.append(element)
    return less, equal, greater


def quick_sort(data: list[Band]) -> list[Band]:
    """
   Performs a quick sort and returns a newly sorted list
   :param data: The data to be sorted (a list)
   :return: A sorted list
   """
    if len(data) == 0:
        return []
    else:
        pivot = data[0]
        less, equal, greater = _partitionQuickSort(data, pivot)
        return quick_sort(less) + equal + quick_sort(greater)


def _partitionQuickSelect(data: list[Band], pivot: Band) -> tuple[list[Band], int, list[Band]]:
    """
   Similar to the partition method that quick sort uses, quick select makes two lists, one for smaller and one
   for greater, and an int that counts the number of elements equal to the pivot.
   :param data: a list of bands to partition
   :param pivot: the element to compare all elements to
   :return: a tuple made of (elements smaller than pivot, count of elements equal to pivot, and elements greater than pivot)
   """
    less, greater = [], []
    count = 0
    for Band in data:
        if Band.votes < pivot.votes:
            less.append(Band)
        elif Band.votes > pivot.votes:
            greater.append(Band)
        else:
            count += 1
    return less, count, greater


def quick_select(data: list[Band], k: int) -> Band:
    """
   quick select calls its own partition method, and then recursively calls itself to shorten the amount of elements
   it will check on its next call. Base case is if pivot k is within the equal partition (aka, the pivot)
   :param data: unsorted list of bands
   :param k: k is the index of the median output (k can be anything, the kth smallest element, more specifically)
   :return: the kth smallest element
   """
    pivot = data[random.randint(0, len(data) - 1)]
    less, equal, greater = _partitionQuickSelect(data, pivot)
    if len(less) <= k < len(less) + equal:
        return pivot
    elif len(less) > k:
        return quick_select(less, k)
    else:
        return quick_select(greater, (k - len(less) - equal))


if __name__ == '__main__':
    main()
