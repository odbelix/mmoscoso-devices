import os
import MySQLdb
import ConfigParser

class DBManager:
	hostname = ""
	username = ""
	password = ""
	database = ""
	databasefile = 'database.ini'
	database = {}
	
	#Get database information from file
	def __init__(self):
		global databasefile
		global database
		
		data = ConfigParser.ConfigParser()
		if os.path.exists(self.databasefile) == False:
			print "ERROR: %s not exists" % self.databasefile
			return False
		else:
			data.read(self.databasefile)
			#Put values to array
			self.database.update({'host':data.get('database','host')})
			self.database.update({'name':data.get('database','name')})
			self.database.update({'user':data.get('database','user')})
			self.database.update({'password':data.get('database','password')})
			self.database.update({'prefix':data.get('database','prefix')})
	
	#Execute query
	def selectValues(self,query):
		global database
		#self.getDataBaseInfo()
		db = MySQLdb.connect(self.database['host'],self.database['user'],self.database['password'],self.database['name'])
		cursor = db.cursor()
		try:
			cursor.execute(query)
			results = cursor.fetchall()
			return results
		except MySQLdb.Error, e:
			print "An error has been passed. %s" %e
			return False

