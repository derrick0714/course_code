'''
Created on Feb 15, 2013

@author: derrick
'''

from models.safe_dic import SafeDictionary

class SameIpHandler(object):
    
    def __init__(self):
        """key ip. value hostname"""
        self._ip_dic   = SafeDictionary()
        
    def check_same_ip(self, html_task):
    
        if  self._ip_dic.has_key(html_task._ip):
            return True
        else: 
            return False
        