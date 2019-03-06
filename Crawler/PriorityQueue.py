#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on Monday 03/04/2019
@author: fanshehu
'''

import heapq

class PriorityQueue:
    '''
    An implementation of priorityqueue based on heapq.
    Entries are object Node.
    '''
    
    def __init__(self):
        # The priorityqueue is implemented by list
        self.queue = []
        # A set which store all urls in priorityqueue
        self.urls = set()
        # A dictionary which maps url to node
        self.dics = {}
        
    class Node:
        
        def __init__(self, priority, url):
            self.priority = priority
            self.url = url
        
        # Comparator for max-heap
        def __lt__(self, other):
            return self.priority > other.priority
        
    '''
    put a new entry to priorityqueue
    item is a tuple like: (priority, url)
    if the url is already in priorityqueue, add priority to it
    '''
    def put(self, item):
        priority, url = item
        if url in self.urls:
            self.dics[url].priority += priority
            heapq.heapify(self.queue)
        else:
            new_item = self.Node(priority, url)
            heapq.heappush(self.queue, new_item)
            self.urls.add(url)
            self.dics[url] = new_item
    
    '''
    pop the entry with greatest priority
    update set and dictionary in the meantime   
    '''
    def pop(self):
        item = heapq.heappop(self.queue)
        del self.dics[item.url]
        self.urls.remove(item.url)
        return (item.priority, item.url)
    
    '''
    return true if the priorityqueue is empty    
    '''
    def is_empty(self):
        return len(self.queue) == 0
