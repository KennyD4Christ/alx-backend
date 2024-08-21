#!/usr/bin/env python3
""" LRUCache module
"""

from base_caching import BaseCaching
from collections import OrderedDict


class LRUCache(BaseCaching):
    """ LRUCache defines a LRU caching system """

    def __init__(self):
        """ Initialize the class """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                # Move the key to the end to show that it was recently used
                self.cache_data.move_to_end(key)
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # Pop the first item (the least recently used)
                oldest_key = next(iter(self.cache_data))
                self.cache_data.pop(oldest_key)
                print(f"DISCARD: {oldest_key}")

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        # Move the key to the end to show that it was recently used
        self.cache_data.move_to_end(key)
        return self.cache_data[key]
