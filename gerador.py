from os import system, makedirs, mkdir, remove, listdir 
from segno import make_qr 
from time import strftime as st
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfReader, PdfMerger
from reportlab.pdfgen import canvas
from webbrowser import open_new_tab as on
import pyodbc as sql
from sqlite3 import connect

class Gerador:
    def __init__(self):
        self.lgConn = connect('src/dd.db')
        self.c = self.lgConn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS USERS(Id INTEGER PRIIMARY KEY, user VARCHAR(100), pwd VARCHAR(100), servidor VARCHAR(100))')

    def excluir(self):
        self.c.execute('delete from USERS')
        self.lgConn.commit()

    def ins(self, uid, pwd, server):
        self.c.execute(f'INSERT INTO USERS(user, pwd, servidor) VALUES ("{uid}","{pwd}","{server}")')
        self.lgConn.commit()
    
    def cons(self):
        self.dd = self.c.execute('SELECT servidor, user, pwd FROM USERS ORDER BY Id DESC').fetchone()
    
    def loginDB(self, server, uid, pwd, dv = '{SQL Server}'):
        if server != ' ' and uid != ' ' and pwd != ' ':
            self.conn = sql.connect(f'DRIVER={dv};SERVER={server};UID={uid};PWD={pwd}')
            self.c2 = self.conn.cursor()

    def logicaDeGeração(self):
        cont = 0
        for c in self.estrutura:
            qrc = c[1] # definindo o qr code
            self.nomeLocal = c[0] # o nome do sublocal
            self.nomeLocal = self.nomeLocal.replace('/','') # removendo barras para n ocasionar erro
            qrcode = make_qr(qrc) # gerando o qrcode.png
            qrLocal = f'{self.nomeDir}\{self.nomeLocal}.png' # definido a estrutura do diretorio
            qrcode.save(qrLocal, scale=10) #salvando o qrcode no diretorio
            qrImg = Image.open(qrLocal) # Abrindo o qrcode com o PIL
            modelo = Image.open(f'src\{self.modelo}.png') # Abrindo o modelo padrão com o PIL
            merge = Image.new('RGBA', modelo.size) # Abrinda uma nova imagem para edição
            x = int((modelo.size[0]-qrImg.size[0])/2) # Valor Dinamico
            merge.paste(modelo) # Carrega o Modelo
            merge.paste(qrImg, (x, 350)) # Cola o qr code no valor relativo
            txt = Image.open(r'src\600.png') # Versionamento de texto
            dw = ImageDraw.Draw(txt) # Esrceve a estrutura e centraliza
            fnt = ImageFont.truetype(r'src\arial_narrow_7.ttf', 35) # Font and size
            x, y = dw.textsize(self.nomeLocal, fnt) # Aplica os valores
            xt = (600-x)/2 # Valor relativo do Texto
            dw.text((xt, 40), self.nomeLocal, font=fnt, fill='black', align='center') # Fazendo o merge do Texto no modelo com o qrcode
            
            # Salva o arquivo!
            txt.save(r'src\texto.png')
            imgt = Image.open(r'src\texto.png')
            x = int((modelo.size[0]-imgt.size[0])/2)
            merge.paste(imgt, (x, 200))
            merge.save(qrLocal)
            
            # Transforma o arquivo em pdf com todos os QRs
            img = Image.open(qrLocal)
            x, y = img.size
            self.nomePdf = f'{self.nomeDir}\{self.nomeLocal}.pdf'
            pdf = canvas.Canvas(self.nomePdf, pagesize=(x, y))
            pdf.drawImage(qrLocal, 0,0)
            pdf.save()
            cont += 1
            
        # MERGE - Mescla os PDF's
        dir = listdir(self.nomeDir)
        mg = PdfMerger()
        for i in dir:
            if '.pdf' in i:
                with open(f'{self.nomeDir}\{i}', 'rb') as arq:
                    dados = PdfReader(arq)
                    mg.append(dados)
        mg.write(f'{self.nomeDir}\EstruturaCompleta.pdf')
        mg.close()
        
        # REMOVE - Remove copias!
        dir = listdir(self.nomeDir)
        for i in dir:
            if '.pdf' in i and i != 'EstruturaCompleta.pdf':
                remove(f'{self.nomeDir}\{i}')
    
    def gerar(self, modelo, CR, nivel):
        if CR != '':
            if nivel != '':
                nivel = 3 + int(nivel)
            elif nivel == '':
                nivel = 3
            self.nivel = nivel
            self.modelo = modelo
            
            self.estrutura = self.c2.execute(f"SELECT E.Descricao as Nome, E.QRCode, E.Grupo FROM Estrutura E INNER JOIN DW_Vista.dbo.DM_Estrutura as Es on Es.Id_Estrutura = Id WHERE Es.CRNo = {CR} AND E.Nivel >= {self.nivel}").fetchall()
            self.cr2 = self.c2.execute(f"select Nivel_03 from DW_Vista.dbo.DM_Estrutura Es with(nolock) where Es.CRNo = '{CR}'").fetchone()[0]
            
            self.data = st('%d-%m_%H-%M-%S')
            try: mkdir(r'QRCodes')
            except: ...
            self.nomeDir = f'QRCodes\{self.cr2}_{self.data}'
            makedirs(self.nomeDir)
            
            self.logicaDeGeração()
        
    def abrirPastaDeGeracao(self):
        try: mkdir(r'QRCodes')
        except: ...
        system('Explorer QRCodes')
        
    def gitHub(self):
        on('https://github.com/foxtec198/Desktop_GQR/issues/new')
        
    def youtube(self):
        on('https://youtu.be/W6hMMplTn0Q')
        
Gerador().cons()    