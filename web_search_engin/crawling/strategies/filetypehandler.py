'''
Created on Feb 14, 2013

@author: Adam57
'''

import mimetypes

class FileTypeHandler(object):
    def FileTypeChecker(self,html_task):
        if mimetypes.guess_type(html_task._url)[0] in ['text/html', None]:
            return True
        else:
            return False