"""
Created on Feb 13, 2013

@author: derrick

"""

from models.status import Status
from models.configuration import Configuration
from include.database import Database
from time import time

class DatabseManager(object):
	def __init__(self, config):
		self._database	= Database(config)
		

	"""
	def write_configuration(self, config):
		sql = "UPDATE\
		`configuation` SET  `downloader_thread` =  {0} ,`downloader_folder`= '{1}',\
		 `parser_thread`= {2}, `seed_keywords`='{3}', `seed_resultnum`={4} WHERE  `configuation`.`id` =1".\
				format(config._down_num, config.download_path, parser_thread, key_words, result_num)

		self._database.execute(sql)	
	"""	

	def write_status(self, status):
		sql = "UPDATE `web_search_engine`.`status` SET `crawled_url_count` = '{0}', `crawled_time` = '{1}', `crawled_size` = '{2}',\
		 `crawled_queue` = '{3}', `parse_count` = '{4}', `parse_queue` = '{5}', `parse_scheme_type` = '{6}', `parse_cgi` = '{7}',\
		  `parse_visited` = '{8}', `parse_robot` = '{9}', `parse_nestlv` = '{10}' WHERE `status`.`id` = 1;"\
			.format( status._download_times, time()-status._sys_start, status._download_size, status._download_queue,\
		 	status._parse_times, status._parse_queue, status._scheme_type, status._cgi, status._early_visit, status._robot, status._nestlv)
		 
		#print sql
		self._database.execute(sql)	
		

	def read_if_start(self, config):
		
		sql = "SELECT `is_start`, `seed_keywords`,`downloader_thread`,`parser_thread`,`seed_resultnum` FROM `configuation` WHERE `id` =1"
		#print sql
		result = self._database.execute(sql)	
		
		if(result[0][0] == True):
			sql = "UPDATE `web_search_engine`.`configuation` SET `is_start` = '0' WHERE `configuation`.`id` = 1"
			self._database.execute(sql)
			
			#update config
			config._keywords = result[0][1]
			config._down_num = result[0][2]
			config._parser_num = result[0][3]
			config._result_num = result[0][4]

			print "####"
			print config._down_num


		if(result != None):
			return result[0][0]
		else:
			return None

	def write_if_start(self):
		 
		sql = "UPDATE `web_search_engine`.`configuation` SET `key_word_start` = '1', `status_start` = '1' WHERE `configuation`.`id` = 1" 
		result = self._database.execute(sql)	
		

	def write_recent_download(self,status):
		for i in range(10):
			html_task = status._recent_url.get(i)
			if html_task._url != "#":
				sql = "INSERT INTO `web_search_engine`.`log` (`url`, `download_time`, `data_size`, `code`, `parent`, `depth`)\
					VALUES ('{0}', now(), '{2}', '{3}', '{4}', '{5}')".format\
					(html_task._url, html_task._crawled_time, html_task._data_size, html_task._return_code, html_task._parent, html_task._depth)
					
				self._database.execute(sql)

