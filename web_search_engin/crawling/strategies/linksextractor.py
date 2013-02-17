'''
Created on Feb 7, 2013

@author: Adam57
'''
import htmllib
import formatter
import urllib

class LinksExtractor(htmllib.HTMLParser):
    
    def __init__(self,formatter):
        htmllib.HTMLParser.__init__(self, formatter)
        """for storing the hyperlinks"""
        self.links = []
        """override handler of <A..>...</A> tags"""
    def start_a(self,attrs):
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0]=="href" :
                    self.links.append(attr[1])
    def get_links(self):
        return self.links
                    
if __name__ == "__main__":
    
        format = formatter.NullFormatter()
        htmlparser = LinksExtractor(format)       
        data = urllib.urlopen("http://cis.poly.edu/index.htm")
        htmlparser.feed(data.read())
        htmlparser.close()
        links = htmlparser.get_links()
        print(links)
        
        
    

        