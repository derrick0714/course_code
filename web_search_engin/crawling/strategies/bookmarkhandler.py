'''
Created on Feb 14, 2013

@author: Adam57
'''
class BookMarkHandler(object):
    
    def BookMarkChecker(self,html_task):
        url = list(html_task._url)
        '''block links starts with #''' 
        if len(url) <= 0: 
            return False
        
        if url[0] == "#":
            return True
        else:
            return False