"""
Created on Feb 13, 2013

@author: derrick

"""

from include.setting import Setting
from include.log import Log

class Configuration(object):
	def __init__(self):

		self._setting = Setting()
	
		#[Downloader]
		self._down_num 		= 0
		self._down_path 	= ""

		#[Parser]
		self._parser_num 	= 0
		self._parser_nlv 	= 0

		#[seed]
		self._keywords 		= ""
		self._result_num 	= 0


		#[Mysql]
		self._host 			= ""
		self._user  		= ""
		self._passwd 		= ""
		self._db 			= ""
	
		self.load()

	"""load all configuration from files or remote mysql"""
	def load(self):
		try:
			
			self._setting.load("config.ini")

			#[Downloader]
			self._down_num 	= int( self._setting.get_param("Downloader","Threadnum") )
			self._down_path	= self._setting.get_param("Downloader","SavePath")

			#[Parser]
			self._parser_num 	= int(self._setting.get_param("Parser","Threadnum"))
			self._parser_nlv 	= int(self._setting.get_param("Parser","Nestlevel"))

			#[seed]
			self._keywords 		= self._setting.get_param("seed","keywords")
			self._result_num 	= int(self._setting.get_param("seed","result_num"))

			#[Mysql]
			self._host 		= self._setting.get_param("Mysql","host")
			self._user  	= self._setting.get_param("Mysql","user")
			self._passwd  	= self._setting.get_param("Mysql","passwd")
			self._db 		= self._setting.get_param("Mysql","db")


		except (Exception) as e:
			Log().debug("load config fail")
			raise(e)
			return False
            
		return True;