'''
Created on Feb 13, 2013

@author: Adam57
'''

from urlparse import urlsplit
from models.html import Html

class NestLevelHandler(object):
    
    def checknestlevel(self, html_task, level):

        if (len(list(set(urlsplit(html_task._url).path.split('/')))) - 1 >= level):
            #print len(list(set(urlsplit(html_task._url).path.split('/')))) - 1
            return True
        else:
            return False
        
        
if __name__ =="__main__":
    h = Html("http://www.test.com/1/2/3/4/5/6")
    n = NestLevelHandler()
    print n.checknestlevel(h,4)
    
    list = "http://www.test.com/1/2/3/4/5/6"
    print list.replace('6','')