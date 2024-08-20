#!/usr/bin/env python3
"""
This module provides a Server class for paginating a dataset of
popular baby names and the index_range function for determining
pagination indices.
"""

import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the start and end index for a given page and page size.

    Args:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start index (inclusive)
                         and end index (exclusive) for the items to be
                         returned on the specified page.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieve a page from the dataset.

        Args:
            page (int): The page number (1-indexed). Must be greater than 0.
            page_size (int): The number of items per page. Must be
            greater than 0.

        Returns:
            List[List]: A list of rows corresponding to the specified page
                        and page_size. Returns an empty list if the range
                        is out of bounds.
        """
        assert isinstance(page, int) and \
            page > 0, "Page number must be a positive integer."
        assert isinstance(page_size, int) and \
            page_size > 0, "Page size must be a positive integer."

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]
