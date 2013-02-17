'''
Created on Feb 13, 2013

@author: Adam57
'''

class CGIHandler(object):

    def FindCGI(self, html_task):
 
        if html_task._url.find(".cgi")==-1:
            return False
        else:
            return True
