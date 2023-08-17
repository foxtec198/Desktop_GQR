# ===============================================================================
# ===============================================================================
# ===============================================================================
# ========================Criado por Guilherme Breve=============================
# ===============================================================================
# ===============================================================================
# ===============================================================================

import pyodbc as sql # Connect SQL
import yaml as y # Yaml de dados
import segno as qr # Gerador de qr
import os # Sistema
from time import strftime as st # Data e Hora Atual

class gerarQrCodes():
    # Função de inicio
    def __init__(self,  *dd):
        self.user = dd[0]
        self.pasw = dd[1]
        self.estrutura = dd[2]
        self.connect()
        self.definir_estrutura()
        self.logica()
    
    # Puxa os dados de um Yaml Codificado!  
    def yml(self):
        with open('dados.yaml', 'r') as f:
            dict = y.load(f, Loader = y.FullLoader)
            self.server = dict['servidor']
            self.db = dict['db']
            self.db02 = dict['db02']
        
    def definir_estrutura(self):
        self.data = st('%d-%m_%H-%M-%S')
        self.consultaSeparada()
        for i in self.estrutura:self.nomeGrupo=i[2]
        self.nomeDir = f'QRCodes\{self.nomeGrupo}_{self.data}'
        os.makedirs(self.nomeDir)
    
    # Logica para gerar qrcodes
    def logica(self): 
        for c in self.estrutura:
            qrc = c[1]
            nomeLocal = c[0]
            qrcode = qr.make_qr(qrc)
            qrcode.save(f'{self.nomeDir}\{nomeLocal}.png', scale=10)
            
    # Conexão com o banco de dados   
    def connect(self):
        # Conecta com o DB
        self.yml()
        st_conn = f"DRIVER=SQL Server; DATABASE={self.db};SERVER={self.server};UID={self.user};PWD={self.pasw}"
        self.conn = sql.connect(st_conn)
        self.c = self.conn.cursor()
        
    def consultaSeparada(self):
        self.cons = f"SELECT Descricao as Nome, QRCode, Grupo FROM Estrutura WHERE HierarquiaDescricao LIKE '%{self.estrutura}%'"
        self.estrutura = self.c.execute(self.cons).fetchall()  
        