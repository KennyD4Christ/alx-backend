#!/usr/bin/env python3
""" LFUCache module
"""

from base_caching import BaseCaching
from collections import defaultdict, OrderedDict


class LFUCache(BaseCaching):
    """ LFUCache defines a LFU caching system """

    def __init__(self):
        """ Initialize the class """
        super().__init__()
        self.cache_data = {}
        self.frequency = defaultdict(int)
        self.usage_order = OrderedDict()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                # Update the item, increase its frequency and mark it as
                # recently used
                self.cache_data[key] = item
                self.frequency[key] += 1
                self.usage_order.pop(key)
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # Find the least frequently used item
                    lfu_keys = [k for k, v in self.frequency.items() if \
                        v == min(self.frequency.values())]
                    # If there is a tie in frequency, find the LRU among the LFU
                    if len(lfu_keys) > 1:
                        lfu_lru_key = next(iter(self.usage_order))
                        for k in lfu_keys:
                            if k == lfu_lru_key:
                                break
                    else:
                        lfu_lru_key = lfu_keys[0]

                    # Remove the LFU/LRU key
                    del self.cache_data[lfu_lru_key]
                    del self.frequency[lfu_lru_key]
                    self.usage_order.pop(lfu_lru_key)
                    print(f"DISCARD: {lfu_lru_key}")

                # Insert the new item
                self.cache_data[key] = item
                self.frequency[key] = 1  # Initialize frequency
            # Mark the key as recently used
            self.usage_order[key] = None

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and mark as recently used
        self.frequency[key] += 1
        self.usage_order.pop(key)
        self.usage_order[key] = None
        return self.cache_data[key]
