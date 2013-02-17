
"""
Created on Feb 2, 2013

@author: derrick

"""
from models.html import Html
from models.safe_loop_array import SafeLoopArray

class Status:
	def __init__(self):
		
		"""--- system ---"""
		self._sys_start			= 0


		"""--- downloads ---"""
		self._download_id		= 0
		self._download_times 	= 0
		self._download_size 	= 0
		self._sites				= 0
		self._recent_url		= SafeLoopArray( Html("#"),10)
		

		"""--- parse ---"""
		self._parse_times		= 0
		self._early_visit		= 0
		self._cgi				= 0
		self._robot				= 0
		self._nestlv			= 0
		self._abandon			= 0
		self._scheme_type		= 0
		self._bookmark			= 0
		self._file_type			= 0




	def get_new_id(self):
		self._download_id = self._download_id+1
		return self._download_id

