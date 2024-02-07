from sqlalchemy import create_engine

engine = create_engine('mssql://guilherme.breve:84584608Guilherme@10.56.6.56/Vista_Replication_PRD?driver=SQL Server')
conn = engine.connect() 

class Logica:
    def __init__(self) -> None:
        pass

    def consultas(self):
        self.cr = ''


class Moldura:
    def __init__(self, **kargs):
        self.modelo = kargs['Modelo']
class QRCode: ...