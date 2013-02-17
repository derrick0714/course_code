'''
Created on Feb 15, 2013

@author: Adam57
'''
class OmitIndex(object):
    def Omit(self, html_task):
        
        url = html_task._url

        url = url.replace('index.htm','')
        url = url.replace('index.html','')
        url = url.replace('index.jsp','')
        url = url.replace('index.asp','')
        url = url.replace('index.php','')
        
        url = url.replace('main.htm','')
        url = url.replace('main.html','')
        url = url.replace('main.jsp','')
        url = url.replace('main.asp','')
        url = url.replace('main.php','')
        
        html_task.update_url(url)
  
        del url