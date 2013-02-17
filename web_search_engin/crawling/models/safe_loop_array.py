"""
Created on Feb 12, 2013

@author: derrick

"""

from threading import Condition
from threading import Lock

class SafeLoopArray(object):
	def __init__(self , data, lengh = 10):
		self._lengh = lengh
		self._data	= []
		self._index = 0;
		self._lock  = Condition(Lock())

		for i in range(lengh):
			self._data.append(data)
			

	def add(self , data):
		self._lock.acquire()
		try:
			i = self._index%self._lengh
			#print "self._lengh = {0},self._index={1},i={2}".format(self._lengh,self._index, i)
			self._data[i] = data
			self._index = self._index+1
		finally:
			self._lock.release()

	def get(self , pos):
		if (pos >= self._lengh):
			print("out of range")
			return None
		self._lock.acquire()
		try:
			return self._data[pos]
		finally:
			self._lock.release()

