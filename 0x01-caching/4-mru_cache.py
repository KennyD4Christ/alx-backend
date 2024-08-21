#!/usr/bin/env python3
""" MRUCache module
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache defines a caching system using the MRU algorithm.
    """

    def __init__(self):
        """ Initialize the MRUCache
        """
        super().__init__()
        self.mru_order = []

    def put(self, key, item):
        """ Add an item in the cache using the MRU algorithm
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.mru_order.remove(key)

        self.cache_data[key] = item
        self.mru_order.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            mru_key = self.mru_order.pop(-2)
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        self.mru_order.remove(key)
        self.mru_order.append(key)
        return self.cache_data[key]
