from core.engine import Engine
from time import sleep
from include.log import Log
import sys


def main():

	try:	
		#create crawler engin
		crawler_engine = Engine()


		#start engine 
		crawler_engine.start( )

		#hold the main thread here, wait for any input to finish
		raw_input("")
		#stop engin 
		crawler_engine.stop()

	except (Exception) as e:  
		Log().debug(e)
		sys.exit(0)
		
if __name__ == "__main__":
	#main(sys.argv[1:])
	main()