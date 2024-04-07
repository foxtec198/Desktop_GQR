from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pandas import read_sql_query as rsq
from segno import make
from functools import cache
from os import mkdir, listdir, system
from time import strftime as st
from shutil import rmtree
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfMerger, PdfReader
from webbrowser import open_new_tab as on
from reportlab.pdfgen import canvas
from sqlite3 import connect

class BackEnd:
    @cache
    def get_cr(self, numCR):
        try:
            cr = rsq(f"SELECT TOP 1 Descricao FROM ESTRUTURA WHERE HierarquiaDescricao LIKE '%{numCR}%'", self.conn)
            for i in cr['Descricao']:
                print(i)
                return i
        except: return 'CR não corresponde'

    @cache
    def definir_cor(self, cr):
        # Azul claro limpeza, laranja logistica, vermelho manutenção, azul escuro segurança e verde jardinagem
        if 'POR -' in cr: return 'src/cores/modeloCinza.png'
        elif 'MAV -' in cr: return 'src/cores/modeloVerde.png'
        elif 'MAP -' in cr: return 'src/cores/modeloVermelho.png'
        elif 'LPG -' in cr: return 'src/cores/modeloAzul.png'
        elif 'SEG -' in cr: return 'src/cores/modeloAzulEscuro.png'
        else: return 'src/cores/modeloAzulEscuro.png'

    @cache
    def get_local(self, numCR, sinal, nivel):
        try: 
            return rsq(f"""
                SELECT Es.QRCode, 
                Es.Descricao as 'Local',
                (SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior' 
                FROM Estrutura Es 
                WHERE HierarquiaDescricao LIKE '%{numCR}%' 
                AND Nivel {sinal} {nivel}""", self.conn)
        except: return "Erro com a consulta!"

    @cache
    def get_link_estrutura(self, numCR):
        try:
            Id = rsq(f"SELECT TOP 1 Id FROM ESTRUTURA WHERE HierarquiaDescricao LIKE '%{numCR}%' AND Nivel = 3", self.conn)
            for id in Id['Id']:
                return f'https://inteligenciaoperacional.app.br/report/gpsvista.php?qrcode={id}'
        except: return 'Link não encontrado'

    @cache
    def set_dataframe(self, cr, nivel=3):
        self.qrs = list() # Cria lista de QRs
        self.local_completo = list() #Cria Lista de Locais Completos
        estrutra = dict()

        cns = self.get_local(cr, nivel) # Consulta os Locais
        for row in cns: # Filtra os dados e manda para as respectivas listas
            self.qrs.append(row[0])
            self.local_completo.append(f'{row[2]} > {row[1]}')
            
        estrutra['QR'] = self.qrs
        estrutra['Local'] = self.local_completo
        return estrutra

    def __init__(self):
        self.database_local()

    @cache
    def login_sql(self, server, uid, pwd, db = 'Vista_Replication_PRD'):
        if server != '':
            server = quote_plus(server)
            if uid != '':
                uid = quote_plus(uid)
                if pwd != '':
                    pwd = quote_plus(pwd)
                    try:
                        db = quote_plus(db)
                        self.engine = create_engine(f"mssql+pyodbc://{uid}:{pwd}@{server}/{db}?driver=ODBC+Driver+17+for+SQL+Server")
                        self.conn = self.engine.connect()
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
        self.lgc = BackEnd()
        try: 
            mkdir('src/temp')
            mkdir('./QRCodes')
        except: ...

    def resizeImg(self, img, valor: tuple):
        imgR = Image.open(img)
        imgR.thumbnail(valor)
        imgR.save(img)

    def gerar_qr(self, cr, nivel):
        if cr != '':
            linkFinal = self.lgc.get_link_estrutura(cr)
            estrutra = self.lgc.set_dataframe(cr, nivel)
            cr = self.lgc.get_cr(cr)
            qrs = estrutra['QR']
            locais = estrutra['Local']
            row = 0
            for local in locais:
                self.makePng(cr, local, qrs[row], linkFinal, row,)
                row += 1
            self.merge(cr)
            rmtree('src/temp')
    
    def makePng(self, crNome, local, qr, link, cont):
            # Gera os QR Codes
            qrlocal = make(qr)
            qrlast = make(link)

            qrlocal.save('src/temp/qrtemp.png', scale=10)
            qrlast.save('src/temp/qrtemp2.png', scale=10)

            self.resizeImg('src/temp/qrtemp.png', (260, 260))
            self.resizeImg('src/temp/qrtemp2.png', (150, 150))

            coresImg = Image.open(self.lgc.definir_cor(crNome))
            logoImg = Image.open('src/logos/ggps.png')
            qrImg = Image.open('src/temp/qrtemp.png')
            qrImg2 = Image.open('src/temp/qrtemp2.png')

            # TEXTO - Nome CR
            textImg = ImageDraw.Draw(coresImg)
            fnt = ImageFont.truetype('src/fonts/arial_narrow_7.ttf', 30)
            txt = f'{crNome[:40]}\n{crNome[40:]}'
            textImg.text((450, 150), txt, font=fnt, fill='black', align='center')

            # TEXTO - Nome Local
            textImg = ImageDraw.Draw(coresImg)
            fnt = ImageFont.truetype('arial', 20)
            txt = f'{local[:40]}\n{local[40:]}'
            textImg.text((450, 210), txt, font=fnt, fill='black', align='center')

            # Cola as propriedas na imagem final
            newImage = Image.new('RGBA', coresImg.size)
            newImage.paste(coresImg)
            newImage.paste(logoImg, (420, 5))
            newImage.paste(qrImg, (75, 100))
            newImage.paste(qrImg2, (755, 410))
            newImage.save('src/temp/temp.png')

            imgQr = Image.open('src/temp/temp.png')
            nomePdf = f'src/temp/{cont}.pdf'
            arquivo = canvas.Canvas(nomePdf, pagesize=imgQr.size, )
            arquivo.drawImage('src/temp/temp.png', 0, 0)
            arquivo.save()

    def merge(self, cr):
        dir = listdir('src/temp/')
        PDF = PdfMerger()
        for i in dir:
            if '.pdf' in i:
                with open(f'src/temp/{i}', 'rb') as pdf:
                    leitura = PdfReader(pdf)
                    PDF.append(leitura)
        PDF.write(f'QRCodes/{cr}.pdf')
        PDF.close()

if __name__ == '__main__':
    b = BackEnd()
    b.login_sql('10.56.6.56', 'guilherme.breve', '84584608@Gui')
    while True:
        QRCode().gerar_qr(input('CR: '), input('Nivel:'))