"""
Created on Feb 12, 2013

@author: derrick

"""
import MySQLdb
from include.log import Log
from models.configuration import Configuration

class Database(object):
	
  def __init__(self, config ):
		self._config 		= config

  def execute(self,sql):
    try: 
      conn = MySQLdb.connect(host=self._config._host,	user=self._config._user, passwd=self._config._passwd, db=self._config._db) 
      conn.autocommit(True)
      cur = conn.cursor()
  			#sql="select * from `status`" 
  			#print sql
      cur.execute(sql)
  			#for row in cur.fetchall() :
     		#		 print row[1]
      return cur.fetchall()
    except (Exception) as e: 
  			Log().debug(e)
  			return None
    finally:
      if conn:
        conn.close()


