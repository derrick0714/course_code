'''
Created on Feb 12, 2013

@author: Adam57
'''

from threading import Condition
from threading import Lock

class SafeDictionary( object ):    
    def __init__(self):
        self._data_dic = {}
        self._lock  = Condition(Lock())


    def addorupdate(self, key, data):
        self._lock.acquire()
        try:
            self._data_dic[key] = data
        finally:
            self._lock.release()
        

    def pop_left(self):
        self._lock.acquire()
        try:
            if ( len(self._data_dic) == 0 ):
                return None
            return self._data_dic.popleft()
        finally:
            self._lock.release()
            
    def clear(self):
        self._lock.acquire()
        try:
            self._data_dic.clear()
        finally:
            self._lock.release()
            
    def has_key(self, key):
        self._lock.acquire()
        try:
            if self._data_dic.has_key(key):
                return True
            else:
                return False
        finally:
            self._lock.release()
            
    def valueofkey(self,key):
        self._lock.acquire()
        try:
            if not self._data_dic.has_key(key):
                return None
            else:
                return self._data_dic[key]
        finally:
            self._lock.release()
