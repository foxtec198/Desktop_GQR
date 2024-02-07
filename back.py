import pyodbc as sql
from segno import make_qr
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
    def get_local(self, numCR, nivel = 3):
        try: return cons(f"SELECT Es.QRCode, Es.Descricao as 'Local', (SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior' FROM Estrutura Es WHERE HierarquiaDescricao LIKE '%{numCR} -%' AND Nivel >= {nivel}")
        except: return "Erro com a consulta!"

    @cache
    def set_dataframe(self, cr, nivel = 3):
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

class QRCode:
    def __init__(self):
        self.lgc = Logica()
        try: 
            mkdir('src/temp')
            mkdir('./QRCodes')
        except: ...

    @cache
    def gerar_qr(self, modelo, cr, nivel = 3):
        if modelo != '':
            self.modelo = modelo
            if cr != '':
                if nivel == None or nivel == '':
                    nivel = 3
                else: 
                    nivel = int(nivel)
                    nivel += 3
                estrutura = self.lgc.set_dataframe(cr, nivel)
                cr = self.lgc.get_cr(cr)

                locais = estrutura['Local']
                qrs = estrutura['QR']
                row = 0
                for local in locais:
                    imgQR = make_qr(qrs[row])
                    imgQR.save('src/temp/qr.png', scale=10)

                    # Abrindo as Imagens
                    imgQR = Image.open('src/temp/qr.png')
                    modelo = Image.open(f'src/{self.modelo}.png')
                    modeloTxt = Image.open('src/600.png')
                    
                    # MONTAGEM
                    novaImagem = Image.new('RGBA', modelo.size)
                    novaImagem.paste(modelo)
                    novaImagem.paste(imgQR, (int((modelo.width - imgQR.width)/2), 350))

                    # TEXTO
                    dw = ImageDraw.Draw(modeloTxt)
                    fnt = ImageFont.truetype('src/arial_narrow_7.ttf', 35)
                    tamanho_do_texto = dw.textlength(local, fnt)
                    x = int((modeloTxt.width - tamanho_do_texto)/2)
                    dw.text((x, 40), local, font=fnt, fill='black', align='center')
                    modeloTxt.save('src/temp/text.png')

                    # Finalizando Montagem
                    imageTxt = Image.open('src/temp/text.png')
                    novaImagem.paste(imageTxt, (int((modelo.size[0] - imageTxt.size[0])/2), 200))
                    novaImagem.save('temp.png')

                    # Cria PDFs temporarios
                    try: mkdir('src/temp/pdfs')
                    except: ...
                    imgQr = Image.open('temp.png')
                    nomePdf = f'src/temp/pdfs/{row}.pdf'
                    arquivo = canvas.Canvas(nomePdf, pagesize=imgQr.size)
                    arquivo.drawImage('temp.png', 0, 0)
                    arquivo.save()
                    row += 1

                self.merge(cr) # Junção dos PDF's
                self.remove_files('src/temp') # Delete dos arquivos temporarios
                return f'QRCodes gerados com sucesso - {cr}'
            else: return 'CR em branco'
        else: return 'Problemas com os modelos!'

    @cache
    def merge(self, cr):
        tm  = st('%d-%m-%Y - %H-%M-%S')
        dir = listdir('src/temp/pdfs')
        PDF = PdfMerger()
        for i in dir:
            if '.pdf' in i:
                with open(f'src/temp/pdfs/{i}', 'rb') as pdf:
                    leitura = PdfReader(pdf)
                    PDF.append(leitura)
        PDF.write(f'QRCodes/{cr} {tm}.pdf')
        PDF.close()

    @cache
    def remove_files(self, dir):
        try: rmtree(dir)
        except: return 'Pasta não encontrada'

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

    @cache
    def abrir_pasta_de_geração(self):
        try: mkdir(r'QRCodes')
        except: ...
        system('Explorer QRCodes')

    @cache    
    def abrir_gitHub(self):
        on('https://github.com/foxtec198/Desktop_GQR/issues/new')
    
    @cache
    def abrir_youtube(self):
        on('https://youtu.be/W6hMMplTn0Q')

if __name__ == '__main__':
    # BackEnd().login_sql('10.56.6.56', 'guilherme.breve','8458Guilherme')
    # QRCode().gerar_qr(17739, 5)
    BackEnd().cons()