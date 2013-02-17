"""
Created on Feb 4, 2013

@author: derrick

"""
import hashlib
from urlparse import urlparse

""" URL model :http://www.webreference.com/html/tutorial2/2.html
http://WebReference.com:80/html/tutorial2/2.html?query
|--|   |--------------||-||--------------------||----|
 1      2               3  4                     5

 1:scheme name :file, ftp, gopher, hdl, http, https, imap, mailto, mms, news, nntp, prospero, rsync, rtsp, rtspu, sftp, shttp, sip, sips, snews, svn, svn+ssh, telnet, wais
 2:hostname
 3:port
 4:path
 5:query_string
"""

class Html(object):

	def __init__(self, url):
		""" related to url"""
		self._url 			= url
		self._scheme 		= ""
		self._hostname		= "" 	#domain name
		self._hostname_hash	= ""
		self._port			= 0
		self._path			= ""
		self._query_string	= ""
		self._md5			= ""
		self._id  			= 0 #increase at engine.finishdownload
		self._depth			= 0 #increase at parser parse_page
		self._parent		= -1 #increase at parser parse_page


		""" analyse url """
		self.parse_url()

		""" related to html data"""
		self._return_code	= ""	#html return code
		self._data			= ""	#html data
		self._data_size		= 0	 	#html size
		self._crawled_time	= 0		#html download time
		

	def update_url(self,url):
		self._url 			= url
		self.parse_url()

	def parse_url(self):
			
		parse_result 		= urlparse(self._url)
		self._scheme 		= parse_result.scheme
		self._hostname		= parse_result.hostname
		self._homesiteurl	= str(parse_result.scheme) + "://" + str(parse_result.hostname)
		#self._hostname_hash	= hashlib.sha256( parse_result.hostname )
		#self._port			= parse_result.port
		self._path			= parse_result.path
		self._query_string	= parse_result.query
		md5 = hashlib.md5()
		md5.update(self._url)
		self._md5 = md5.hexdigest()	
		#print(self._md5)
		
		
		
if __name__=="__main__":
	html = Html("http://www.nba.com/standings/team_record_comparison/conferenceNew_Std_Cnf.html")
	print html._homesiteurl
