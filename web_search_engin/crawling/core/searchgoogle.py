'''
Created on Feb 10, 2013

@author: Adam57
'''

import urllib2,urllib
import json
from include.log import Log

class SearchGoogle(object):
    def __init__(self, searchstr = 'NYU', resultnum = 10):
        self._keywords = searchstr
        self._links = []
        self._result_num = resultnum
    def getURLs(self):
        for x in range(self._result_num):   
            #start = x*1           
            url = ('https://ajax.googleapis.com/ajax/services/search/web'
                  '?v=1.0&q=%s&rsz=1&start=%s') % (urllib.quote(self._keywords),x)
            try:
                request = urllib2.Request(url, None, {'Referer':'http://www.nyu.edu'})
                response = urllib2.urlopen(request)

                """Process the JSON string."""
                results = json.load(response)
                info = results['responseData']['results']
            except Exception,e:
                Log().debug(e)
            else:
                for minfo in info:
                    self._links.append(minfo['url'])
                    # print(minfo['url'])
            finally:
                response.close()

        return self._links        
                
if __name__ == "__main__": 
    contacter = SearchGoogle("Torsten Suel",15)    
    print(contacter.getURLs())
    