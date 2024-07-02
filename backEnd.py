from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pandas import read_sql
import pyodbc as sql

class BackEnd:
    def new_connect_db(self, uid, pwd, server, database='Vista_Replication_PRD', driver='ODBC Driver 18 for SQL Server'):
        self.uid = quote_plus(uid)
        self.pwd = quote_plus(pwd)
        self.server = quote_plus(server)
        self.database = quote_plus(database)
        driver = quote_plus(driver)
        url = f'mssql://{self.uid}:{self.pwd}@{self.server}/{self.database}?driver={driver}&&TrustServerCertificate=yes'
        try:
            engine = create_engine(url)
            return engine
        except Exception as error:
            return error

if __name__ == '__main__':
    con = BackEnd().new_connect_db('guilherme.breve','84584608-Gui','10.56.6.56')
    conn = con.connect()
    a = read_sql('select top 1 nome from tarefa', conn)
    print(a)