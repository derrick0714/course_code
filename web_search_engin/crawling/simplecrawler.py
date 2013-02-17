'''
Created on Feb 2, 2013

@author: Adam
'''
import re 
#import urllib.request #python3.3
import urllib
import lxml

"""

textfile = open("depth_1.txt","wt")

#for i in re.findall(b'''href=["'](.[^"']+)["']''', urllib.request.urlopen("http://cis.poly.edu/cs6913/").read(), re.I):
for i in re.findall(b'''href=["'](.[^"']+)["']''', urllib.urlopen("http://cis.poly.edu/cs6913/").read(), re.I):
    print (i)
    textfile.write(i.decode("utf-8")+'\n')
    #for ee in re.findall(b'''href=["'](.[^"']+)["']''', urllib.request.urlopen("http://cis.poly.edu/cs6913/"+i.decode("utf-8")).read(), re.I):
    for ee in re.findall(b'''href=["'](.[^"']+)["']''', urllib.urlopen("http://cis.poly.edu/cs6913/"+i.decode("utf-8")).read(), re.I):
        print (ee)
        textfile.write(ee.decode("utf-8")+'\n')

textfile.close()

"""
url = "http://www.google.com/cgi.test.cgi.cgicgicgi"
print (url.find("cgi"))