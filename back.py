import pyodbc as sql
from segno import make
from functools import cache
from os import mkdir, listdir, system, remove
from time import strftime as st
from shutil import rmtree
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfMerger, PdfReader
from webbrowser import open_new_tab as on
from reportlab.pdfgen import canvas
from sqlite3 import connect

def cons(consulta):
    return c.execute(consulta).fetchall()

class Logica:
    @cache
    def get_cr(self, numCR):
        try:
            cr = cons(f"SELECT TOP 1 Descricao FROM ESTRUTURA WHERE HierarquiaDescricao LIKE '%{numCR} - %' AND Nivel = 3")[0][0]
            return cr
        except: return 'CR não corresponde'

    @cache
    def get_local(self, numCR, nivel=3):
        try: return cons(f"SELECT Es.QRCode, Es.Descricao as 'Local', (SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior' FROM Estrutura Es WHERE HierarquiaDescricao LIKE '%{numCR} -%' AND Nivel >= {nivel}")
        except: return "Erro com a consulta!"

    @cache
    def set_dataframe(self, cr, nivel=3):
        self.qrs = list() # Cria lista de QRs
        self.local_completo = list() #Cria Lista de Locais Completos
        estrutra = dict()

        cns = self.get_local(cr, nivel) # Consulta os Locais
        for row in cns: # Filtra os dados e manda para as respectivas listas
            print(row)
            # self.qrs.append(row[0])
            # self.local_completo.append(f'{row[2]} > {row[1]}')
            
        estrutra['QR'] = self.qrs
        estrutra['Local'] = self.local_completo
        return estrutra

class BackEnd:
    def __init__(self):
        self.database_local()

    @cache
    def login_sql(self, server, uid, pwd):
        global c, engine
        if server != '':
            if uid != '':
                if pwd != '':
                    try:
                        engine = sql.connect(f'DRIVER=SQL Server;UID={uid};PWD={pwd};SERVER={server};DATABASE=Vista_Replication_PRD')
                        c = engine.cursor()
                        return 'Logado com Sucesso'
                    except: return 'Conexão Invalida!'
                else: return 'Senha Vazia'
            else: return 'Usuário Vazio'
        else: return 'Server Vazio'


    def database_local(self):
        try: mkdir('./src')
        except: ...
        self.lgConn = connect('src/dd.db')
        self.c = self.lgConn.cursor()
        try:
            self.c.execute('CREATE TABLE IF NOT EXISTS USERS(Id INTEGER PRIIMARY KEY, user VARCHAR(100), pwd VARCHAR(100), servidor VARCHAR(100))')
        except: ...

    def limpar_database(self):
        self.c.execute('delete from USERS')
        self.lgConn.commit()

    def cons(self):
        self.dd = self.c.execute('SELECT servidor, user, pwd, Id FROM USERS ORDER BY Id DESC').fetchone()

    def ins(self, server, uid, pwd):
        self.cons()
        if self.dd != None: 
            idEx = self.dd[3]
            self.c.execute(f'DELETE FROM USERS WHERE Id <> {idEx}')
        self.c.execute(f'INSERT INTO USERS(user, pwd, servidor) VALUES ("{uid}","{pwd}","{server}")')
        self.lgConn.commit()

    def abrir_pasta_de_geração(self):
        try: mkdir(r'QRCodes')
        except: ...
        system('Explorer QRCodes')

    def abrir_gitHub(self):
        on('https://github.com/foxtec198/Desktop_GQR/issues/new')
    
    def abrir_youtube(self):
        on('https://youtu.be/W6hMMplTn0Q')

class QRCode:
    def __init__(self) -> None:
        try: mkdir('src/temp')
        except: ...

    def resizeImg(self, img, valor: tuple):
        imgR = Image.open(img)
        imgR.thumbnail(valor)
        imgR.save(img)

    def gerar_qr(self, cr, nivel=3):
        if cr != '':
            if nivel == '' or nivel == None:
                nivel = 3
            else: 
                nivel = int(nivel)
                nivel += 3

            estrutra = l.set_dataframe(cr, nivel)
            cr =   l.get_cr(cr)
            qrs = estrutra['QR']
            locais = estrutra['Local']
            row = 0
            for local in locais:
                self.makePng(cr, local, qrs[row], 'teste')
                row += 1
    
    def makePng(self, cr, local, qr, link):
            # Gera os QR Codes
            qrlocal = make(qr)
            qrlast = make(link)

            qrlocal.save('src/temp/qrtemp.png', scale=10)
            qrlast.save('src/temp/qrtemp2.png', scale=10)

            self.resizeImg('src/temp/qrtemp.png', (260, 260))
            self.resizeImg('src/temp/qrtemp2.png', (150, 150))

            coresImg = Image.open('src/cores/modeloVerde.png')
            logoImg = Image.open('src/logos/ggps.png')
            qrImg = Image.open('src/temp/qrtemp.png')
            qrImg2 = Image.open('src/temp/qrtemp2.png')


            # TEXTO - Nome CR
            textImg = ImageDraw.Draw(coresImg)
            fnt = ImageFont.truetype('src/arial_narrow_7.ttf', 30)
            textImg.text((500, 150), cr, font=fnt, fill='black', align='center')

            # TEXTO - Nome Local
            textImg = ImageDraw.Draw(coresImg)
            fnt = ImageFont.truetype('arial', 25)
            textImg.text((500, 200), local, font=fnt, fill='black', align='center')

            newImage = Image.new('RGBA', coresImg.size)
            newImage.paste(coresImg)
            newImage.paste(logoImg, (420, 5))
            newImage.paste(qrImg, (75, 100))
            newImage.paste(qrImg2, (755, 410))
            newImage.save('temp.png')


if __name__ == '__main__':
    b = BackEnd()
    q = QRCode()
    l = Logica()
    print(b.login_sql('10.56.6.56','guilherme.breve','8458Guilherme'))
    # q.gerar_qr(17739, 2)