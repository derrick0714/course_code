"""
Created on Feb 4, 2013

@author: derrick

"""
from threading import Thread

class Command(Thread):

	def __init__( self ):
		Thread.__init__(self) 

	def run( self ):
		print "in command, hah" 
	
