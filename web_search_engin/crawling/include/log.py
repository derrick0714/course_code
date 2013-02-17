"""
Created on Feb 1, 2013

@author: Adam57

This part takes care of the logging
"""
import os 
import time 
import logging 
import inspect
import sys, traceback

class Log(object):	 
    def __init__(self): 
        self.__logger = logging.getLogger() 
        path = os.path.abspath("Log.log") 
        handler=logging.FileHandler(path) 
        self.__logger.addHandler(handler) 
        self.__logger.setLevel(logging.WARNING)
    def getLogMessage(self,level,message):
        frame,filename,lineNo,functionName,code,otherinfo = inspect.stack()[2]        
        return "[%s] [%s] [%s - %s - %s] %s" %(self.printfNow(),level,filename,lineNo,functionName,message)
    def info(self,message): 
        message = self.getLogMessage("info",message) 
        print(message)
        self.__logger.info(message)
    def error(self,message): 
        message = self.getLogMessage("error",message)
        print(message)
        self.__logger.error(message)
    def warning(self,message): 
        message = self.getLogMessage("warning",message)
        print(message) 
        self.__logger.warning(message)
    def debug(self,message): 
        message = self.getLogMessage("debug",message) 
        print(message)
        traceback.print_exc(file=sys.stdout)
        self.__logger.debug(message)
    def critical(self,message): 
        message = self.getLogMessage("critical",message) 
        print(message)
        self.__logger.critical(message)
    def printfNow(self): 
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    def write(self, string):
        print(string)	


if __name__ == "__main__": 
    logger = Log() 
    logger.info("hello")
    logger.warning("hello")

