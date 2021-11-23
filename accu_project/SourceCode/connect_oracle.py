import cx_Oracle

USER = ""
PASSWORD = ""
DNS = "localhost/xepdb1"

class OracleDatabase:
  connection = None
  cursor = None
  
  def __init__(self):
    self.connection = cx_Oracle.connect(
			user=USER,
			password=PASSWORD,
			dsn=DNS)
  	
   	self.cursor = self.connection.cursor()

	def run_query(self, query):
		for row in self.cursor.execute(query):
			print(row)
   
		self.connection.commit()
