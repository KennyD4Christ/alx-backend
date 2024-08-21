#!/usr/bin/env python3
""" FIFOCache module
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache defines a FIFO caching system """

    def __init__(self):
        """ Initialize the class """
        super().__init__()
        self.cache_order = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            if key not in self.cache_data:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    first_key = self.cache_order.pop(0)
                    del self.cache_data[first_key]
                    print(f"DISCARD: {first_key}")
            self.cache_data[key] = item
            if key not in self.cache_order:
                self.cache_order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key, None)
