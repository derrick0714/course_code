'''
Created on Feb 2, 2013

@author: Adam
'''
#import configparser #python3.3
import ConfigParser


class Setting(object):   
    
    def load(self, path):
        self.path = path 
              
    def get_section(self, section):
        #conf = configparser.ConfigParser() #python3.3
        conf = ConfigParser.ConfigParser()
        conf.read(self.path)
        return conf.items(section)
    
    def get_param(self, section, param):
        #conf = configparser.ConfigParser() #python3.3
        try:
            conf = ConfigParser.ConfigParser()
            conf.read(self.path)
            return conf.get(section,param)
        except (Exception) as e:
            raise(e)
    
    def set_param(self, section, param, new_value):
        #conf = configparser.ConfigParser() #python3.3
        conf = ConfigParser.ConfigParser()
        conf.read(self.path)
        conf.set(section, param, new_value)
        conf.write(open(self.path, "w"))
        
    def add_param(self, section, new_param, new_value):
        #conf = configparser.ConfigParser() #python3.3
        conf = ConfigParser.ConfigParser()
        conf.read(self.path)
        conf.set(section, new_param, new_value)
        conf.write(open(self.path, "w"))  
#"c:\\config.ini" 

    
if __name__ == "__main__": 
    config = Setting() 
    config.load("c:\\config.ini" );
    print (config.get_section("log"))
    config.set_param("log", "L1", "trial")   
    print (config.get_section("log"))
    config.add_param("log","L4", "new trial") 
    print (config.get_section("log"))    
    print(config.get_param("log","L4"))
    
    
        