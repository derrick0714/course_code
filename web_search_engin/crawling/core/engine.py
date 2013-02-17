
"""
Created on Feb 2, 2013

@author: derrick

"""
#import basic lib
from threading import Thread	    
from time import time, sleep,localtime,strftime
import os

#import core lib
from core.downloader import Downloader
from core.parser import Parser
from core.searchgoogle import SearchGoogle

#import auxiliary lib
from include.log import Log
from include.database_manager import DatabseManager

#import modles
from models.html import Html
from models.status import Status
from models.safe_queue import SafeQueue
from models.safe_loop_array import SafeLoopArray
from models.safe_dic import SafeDictionary
from models.configuration import Configuration

#include strategies
from strategies.robothandler import RobotHandler
from strategies.earlyvisithandler import EarlyVisitHandler
from strategies.cgihandler import CGIHandler
from strategies.nestlevelhandler import NestLevelHandler
from strategies.schemehandler import SchemeHandler
from strategies.filetypehandler import FileTypeHandler
from strategies.bookmarkhandler import BookMarkHandler
from strategies.urlextender import URLExtender
from strategies.omitindex import OmitIndex



class Engine(object):
	def __init__( self):
		self._istart		= False
		self._status		= Status()

		"""--- load config file----"""
		self._config 		= Configuration();
	
		"""--- core object ----"""
		self._downloader	= None
		self._parser		= Parser( self._config._down_num, self._status )

		"""--- memory models --- """
		self._download_pool	= SafeQueue() #Store the html objects to be downloaded by the downloader
		self._parse_pool	= SafeQueue() #Store the html objects to be parsed by the parser
		
		"""--- checker threads --- """
		"""The target is the function passed in to 
		run in the thread. Those two threads keep checking 
		and assigning jobs to the two thread pools"""
		self._downloader_pool_checker = Thread( target=self.download_pool_checker)
		self._parse_pool_checker = Thread( target=self.parse_pool_checker)
		
		"""---  threads --- """
		self._status_update = Thread( target=self.status_update) #every second, this thread post runtime info to remote mysql

		""" ---strategies--- """
		self._earlyvisithandler	=	EarlyVisitHandler()
		self._robothandler  	=	RobotHandler()
		self._cgihandler		=	CGIHandler()
		self._nestlevelhandler 	=	NestLevelHandler()
		self._schemehandler    	=	SchemeHandler()
		self._filetypehandler	=	FileTypeHandler()
		self._bookmarkhandler	=	BookMarkHandler()
		self._omitindex			=	OmitIndex()
		self._urlextender		=	URLExtender()			
	
		""" ---init the path for saving data, if the folder don't exist, create it ---"""
		self._path			= self._config._down_path+"/"+ strftime('%Y-%m-%d', localtime())+"/"+ strftime('%H-%M-%S', localtime())+"/"
		if not os.path.exists(self._path):
			os.makedirs(self._path)

		self._config._down_path = self._path
		
		self._keywords_links= []

		""" ---Mysql Manager--- """
		self.sqlex      = DatabseManager(self._config)

	def load_seeds(self):
		#load seed info from config file	
		#print "load_seeds 1"
		#load seed from 
		contacter = SearchGoogle(self._config._keywords, self._config._result_num)
		self._keywords_links = contacter.getURLs()
		#append seeds, which from google search result, into download pool
		#print "load_seeds 2"
		#self._keywords_links.insert(0, "https://twitter.com/")
		#self._keywords_links.insert(0, "https://twitter.com/signup?context=login")
		
		i = 0
		for url in self._keywords_links:
			if i < self._config._result_num:
				#print "@@{0}".format(url)
				html_task = Html(url)

				#print "@@1"
				if(self._schemehandler.SchemeChecker(html_task)==False):
					#print("Ingore the wrong scheme, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
					#print "@@2"
					self._status._scheme+=1
					continue
				if(self._bookmarkhandler.BookMarkChecker(html_task)==True):
					#print("Ingore bookmark link, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
					#print "@@3"
					self._status._bookmark+=1
					continue
				if(self._cgihandler.FindCGI(html_task)==True):
					#print("Ingore the link contain cgi, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
					#print "@@4"
					self._status._cgi+=1
					continue
				if(self._nestlevelhandler.checknestlevel(html_task,self._config._parser_nlv)==True):
					self._status._nestlv +=1
					#print "@@5"
					#print("Ingore the link nested too much, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
					continue
				if(self._filetypehandler.FileTypeChecker(html_task)==False):
					#print "@@6"
					self._status._file_type +=1
					continue
				#print "@@7"
				'''
				if(self._earlyvisithandler.check_visited(html_task) == True):
					self._status._early_visit +=1
					#print("Ingore the link visited before, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
					continue
				'''
				self._omitindex.Omit(html_task)
				"""
				print "@@8"
				if(self._robothandler.is_allowed(html_task) == False):
					print "@@9"
					self._status._robot +=1
					#print("Blocked by the Robot.txt, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
					continue
				print "@@10"
				"""
				self._earlyvisithandler.add_entry(html_task._md5, html_task)
				self._download_pool.append(html_task)
				'''If use the following two line of code, then the program won't run, which means checking for revisit works'''
				'''however, the dic should be safe with a lock'''
				#self._visited_dic[html_task._md5] = html_task._url 
				#print(len(self._visited_dic))
				#print "@@11"
			else:

				break
			i+=1
		#print "load_seeds 3"
	def show_welcome(self):
		print("download folder:"+self._path)
		print "key words:"+self._config._keywords
		print "donload thread num: {0}".format(self._config._down_num)
		print "parse thread num: {0}".format(self._config._parser_num)
		print "Load " +str(self._config._result_num)+" results from google search:"
		
		i = 0
		for url in self._keywords_links:
			if i < self._config._result_num:
				print ("[{0}]".format(i)+url)
			i+=1
		

		#raw_input("press any key to start crawling, press second key to stop")
	
	def wait_for_start(self):
		print "ready for start....."
		while( self.sqlex.read_if_start(self._config)!= True):
			sleep(1)
		print "starting crawling engine...."

	def start(self):
		try:
			self.wait_for_start()

			self._istart = True
			
			"""load seed """
			self.load_seeds()	#load seeds from google search 

			
			"""show welcome info"""
			self.show_welcome()
			self._status._sys_start	= time()

			"""start threads"""
			self._downloader = Downloader( self._config._down_num, self._status)
			self._downloader.start()
			self._parser.start()
			self._downloader_pool_checker.start()
			self._parse_pool_checker.start()
			self._status_update.start()


			"""notify mysql, i am started"""
			self.sqlex.write_if_start()
			
		except (Exception) as e:
			Log().debug("start failed")
			raise(e)
			return False

		
		
	def stop(self):
		self._istart = False
		""""clear download and parse popl"""
		self._download_pool.clear()
		self._parse_pool.clear()

		"""stop downloader and parser threads"""
		self._downloader.stop()
		self._parser.stop()
		""""Those two checker threads will end when the thread who calls them ends"""
		self._downloader_pool_checker.join()
		self._parse_pool_checker.join()
		self._status_update.join()
		print ("Engine is stopping")

	def pause(self):
		pass

	def finish_download(self, html_task):
			
		"""
		print("Downloaded:[No.{0}] time:{1:0.1f} page:depth_parent {2}_{3} http-status: {4} data-size: {5}byes url:{6}"\
			.format(self._status._download_times,time()-self._status._sys_start,html_task._depth,\
		html_task._parent,html_task._return_code, html_task._data_size, html_task._url))
		"""

		"""caculate the path for saving files"""
		full_path = self._path+"[No.{0}]_".format(self._status._download_times)+".html"

		"""save html data to files"""
		#f= open(full_path, 'w')
		#f.write(html_task._data)
		#f.close()


		"""After downloading, pass the data(still using the html objects) to the parse pool"""
		self._parse_pool.append(html_task)




	def finish_parse(self, html_task):
		'''
		print("parsed:[No.{0}] time:{1:0.1f} page:depth_parent {2}_{3} http-status: {4} data-size: {5}byes url:{6}"\
			.format(self._status._download_times,time()-self._status._sys_start,html_task._depth,\
		html_task._parent,html_task._return_code, html_task._data_size, html_task._url))
		'''
		"""After parsing, pass the urls to be downloaded to the download pool"""
		if(self._earlyvisithandler.check_visited(html_task) == True):
			#print("Ingore the link visited before, this link is within page {0} , so don't put it in queue".format(html_task._parent), html_task._url)
			self._status._early_visit +=1
			return
		if(self._robothandler.is_allowed(html_task) == False):
			#print("Blocked by the Robot.txt, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
			self._status._robot +=1
			return
		
		self._earlyvisithandler.add_entry(html_task._md5, html_task)
		self._download_pool.append(html_task)
		




	def download_pool_checker(self):
		while (self._istart == True):
			new_download_task = self._download_pool.pop_left()
			"""If there is no task remain in the download pool, put the thread into sleep"""
			"""else pop the new task, and download it"""
			"""for the engine to get the result to put into the parse pool, we need to pass the function finish_download down as a callback"""
			if (new_download_task == None):
				#print("No task remaining in download_pool")
				sleep(0.1)
			else:
				self._downloader.queue_download_task(new_download_task , self.finish_download)


	def parse_pool_checker(self):
		while (self._istart == True):
			new_parse_task = self._parse_pool.pop_left()
			if (new_parse_task == None):
				#print("sleeping")
				sleep(0.1)				
			else:

				self._parser.queue_parse_task(new_parse_task, self.finish_parse)





	#~~~see result at http://dengxu.me/crawling/
	def status_update(self):

		while (self._istart == True):

			self._status._download_queue = self._downloader.len()
			self._status._parse_queue = self._parser.len()
			
			print "[time: {0:0.1f}],queue:{8}, down: {1}, total: {2:0.1f}MB | queue:{9}, parsed: {3}, scheme:{10}, cig: {4}, bookmark: {11} type {12} visited: {5}, robot: {6},nestlv: {7}"\
			.format( time()-self._status._sys_start,\
		 	self._status._download_times, float(self._status._download_size)/1024/1024, self._status._parse_times\
		 	,self._status._cgi, self._status._early_visit, self._status._robot, self._status._nestlv\
		 	,self._downloader.len(), self._parser.len(),self._status._scheme_type, self._status._bookmark, self._status._file_type)
			
			"""update status tp mysql"""
			self.sqlex.write_status(self._status)
			
			"""update recent download url"""
			self.sqlex.write_recent_download(self._status)
			
			sleep(1)
	"""	
		sql = "UPDATE  `configuation` SET  `downloader_thread` =  {0} ,`downloader_folder`= '{1}', `parser_thread`= {2}, `seed_keywords`='{3}', `seed_resultnum`={4} WHERE  `configuation`.`id` =1".\
				format(self._setting.get_param("Downloader","Threadnum"), self._path, self._setting.get_param("Parser","Threadnum"),self._keywords,self._result_num)
		
		self._database.execute(sql)
		
		#update result url
		sql = "DELETE FROM `key_words`"
		self._database.execute(sql)
		for links in self._keywords_links:
			sql = "INSERT INTO `web_search_engine`.`key_words` (`id`, `url`) VALUES (NULL, '{0}')".format(links)
			self._database.execute(sql)

		while (self._istart == True):
			sql = "UPDATE  `status` SET  `crawled_url_count` =  '{0}'  WHERE  `status`.`id` =1".format(self.download_times)
			self._database.execute(sql)


			for i in range(10):
				html_task = self._last_log.get(i)
				if html_task._url != "#":
					sql = "INSERT INTO `web_search_engine`.`log` (`url`, `download_time`, `data_size`, `code`, `parent`, `depth`)\
						VALUES ('{0}', now(), '{2}', '{3}', '{4}', '{5}')".format\
						(html_task._url, html_task._crawled_time, html_task._data_size, html_task._return_code, html_task._parent, html_task._depth)
					
					self._database.execute(sql)

			sleep(1)
	"""

		
   


