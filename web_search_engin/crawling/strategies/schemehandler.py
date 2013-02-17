'''
Created on Feb 14, 2013

@author: Adam57
'''
class SchemeHandler(object):
    def SchemeChecker(self, html_task):
        
        #print (html_task._url, html_task._scheme, html_task._hostname, html_task._path, html_task._query_string)
        '''block url links less or equal than 0'''
        url = list(html_task._url)
        if len(url) <= 0: 
            return False
                
        '''scheme white list'''
        if not html_task._scheme in ['http', 'https', ""]:
            return False   
        #if (html_task._hostname == None and html_task._path == ""):       
 
        return True