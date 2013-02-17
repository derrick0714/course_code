'''
Created on Feb 14, 2013

@author: Adam57
'''
class URLExtender(object):
    def ExtendURL(self, child, parent):
        if child._url =="/":
            child.update_url(parent._url)  
            #print child._url
       # parent._url = parent._url
       	if(child._url[0] == '/'):
       		child._url = child._url[1:]
       		#print child._url 
        child.update_url(parent._url + child._url)
       # child._url
        