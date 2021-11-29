import cx_Oracle
       
USER = "smartw_view_only"
PASSWORD = "smartw_view_only"
DNS = "10.16.150.77:1521/soca"

class OracleDatabase:
  connection = None
  cursor = None
  
  def __init__(self):
    self.connection = cx_Oracle.connect(user=USER, password=PASSWORD, dsn=DNS)
    self.cursor = self.connection.cursor()

  def _dictfetchall(self):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in self.cursor.description]
    return [
        dict(zip(columns, row))
        for row in self.cursor.fetchall()
    ]
    
  def _dictfetchone(self):
    "Return one row from a cursor as a dict"
    columns = (col[0] for col in self.cursor.description)
    result = self.cursor.fetchone()
    result = dict(zip(columns, result))
    return result

  def run_query(self, query):
    self.cursor.execute(query)
    #self.connection.close()
    return self._dictfetchall()

