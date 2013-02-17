'''
Created on Feb 6, 2013

@author: Adam57
'''
from models.html import Html 
from include.thread_pool import ThreadPool
from include.log import Log
from include.setting import Setting
from strategies.linksextractor import LinksExtractor
from models.safe_queue import SafeQueue
import urllib, formatter
from models.status import Status
from models.configuration import Configuration
from strategies.cgihandler import CGIHandler
from strategies.nestlevelhandler import NestLevelHandler
from strategies.schemehandler import SchemeHandler
from strategies.filetypehandler import FileTypeHandler
from strategies.bookmarkhandler import BookMarkHandler
from strategies.urlextender import URLExtender
from strategies.omitindex import OmitIndex


class Parser(object):
   
    def __init__(self, num_thread, status):
        self._num_threads = num_thread
        self._parse_workers = ThreadPool(num_thread)
        self._parsing_depth = 0
        self._parsing_id = 0
        self._status            = status
        self._cgihandler        =    CGIHandler()
        self._nestlevelhandler     =    NestLevelHandler()
        self._schemehandler        =    SchemeHandler()
        self._filetypehandler    =    FileTypeHandler()
        self._bookmarkhandler    =    BookMarkHandler()
        self._urlextender        =    URLExtender()
        self._filetypehandler   =   FileTypeHandler()
        self._omitindex            =    OmitIndex()
        self._config            =   Configuration()
                
    def queue_parse_task(self, html_task, callback):
        """assign the tasks(function, parameter, and callback) to the workers(thread pool)"""
        self._parse_workers.queue_task(self.parse_page, html_task, callback)

    def start(self):
        self._parse_workers.start()

    def stop(self):
        self._parse_workers.stop()

    def len(self):
        return self._parse_workers.get_queue_count()
    
    def parse_page(self, html_task, callback):
        
        links = []
        format = formatter.NullFormatter()
        htmlparser = LinksExtractor(format)
        self._parsing_depth = html_task._depth
        self._parsing_id = html_task._id
        try:     
            htmlparser.feed(html_task._data)
            htmlparser.close()
            links = htmlparser.get_links()
        except (Exception) as e:
            #print(html_task._data)
            print(html_task._url)
            Log().debug(e)
        #finally:
        #    del html_task


        for link in links:
            #print (link)
            
            html_task_child = Html(link)
            
            self._status._parse_times+=1

            """load all strategies to determine if this link can be download"""
            if(self._schemehandler.SchemeChecker(html_task_child)==False):
                #print("Ingore the wrong scheme, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
                self._status._scheme_type+=1
                continue                  
            if(self._bookmarkhandler.BookMarkChecker(html_task_child)==True):
                #print("Ingore bookmark link, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
                self._status._bookmark+=1
                continue
            if(self._cgihandler.FindCGI(html_task_child)==True):
                #print("Ingore the link contain cgi, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
                self._status._cgi+=1
                continue        
            if(self._nestlevelhandler.checknestlevel(html_task_child,self._config._parser_nlv)==True):
                #print("Ingore the link nested too much, this link is within page {0} , so don't download".format(html_task._parent), html_task._url)
                self._status._nestlv +=1
                continue        
            if(self._filetypehandler.FileTypeChecker(html_task_child)==False):
                self._status._file_type +=1
                continue
            
            self._omitindex.Omit(html_task)
            
            if(html_task_child._scheme == "" and html_task_child._hostname==None):
                self._urlextender.ExtendURL(html_task_child, html_task)
                                   
            #if self.parse_link( html_task_child ) == True:
           
            html_task_child._depth = self._parsing_depth+1
            html_task_child._parent = self._parsing_id
            callback(html_task_child)

        del html_task
    '''      
    def parse_link(self, html_task ):
        self._status._parse_times+=1
        
        '
        #simple filter of no _scheme & _hostname for test
        
        if (html_task._scheme =="") | (html_task._hostname == ""):
            #print("no _scheme & _hostname ")
            self._status._abandon+=1
            return False
      
        
        #simple filter of type of scheme for test
        
        if html_task._scheme !="http":
            #print(" html_task._scheme={0}".format(html_task._scheme))
            self._status._abandon+=1
            return False
        
        return True
    '''