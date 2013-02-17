'''
Created on Feb 13, 2013

@author: Adam57
'''

from models.safe_dic import SafeDictionary

class EarlyVisitHandler(object):
    
    def __init__(self):
        """this dic stores normlized url(md5) and the html"""
        self._visited_dic   = SafeDictionary()
        
    def check_visited(self, html_task):
    
        if  self._visited_dic.has_key(html_task._md5):
            return True
        else: 
            return False
    
    def add_entry(self,key,value):
        self._visited_dic.addorupdate(key, value)
