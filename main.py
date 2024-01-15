# imports Front
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.toast import toast
#Imports Back
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
        try: mkdir('./_internal/src')
        except: ...
        self.lgConn = connect('_internal/src/dd.db')
        self.c = self.lgConn.cursor()
        try:
            self.c.execute('CREATE TABLE IF NOT EXISTS USERS(Id INTEGER PRIIMARY KEY, user VARCHAR(100), pwd VARCHAR(100), servidor VARCHAR(100))')
        except: ...
        
    def excluir(self):
        self.c.execute('delete from USERS')
        self.lgConn.commit()

    def ins(self, uid, pwd, server):
        idEx = self.dd[3]
        self.c.execute(f'DELETE FROM USERS WHERE Id <> {idEx}')
        self.c.execute(f'INSERT INTO USERS(user, pwd, servidor) VALUES ("{uid}","{pwd}","{server}")')
        self.lgConn.commit()
    
    def cons(self):
        self.dd = self.c.execute('SELECT servidor, user, pwd, Id FROM USERS ORDER BY Id DESC').fetchone()
    
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
            modelo = Image.open(f'_internal/src\{self.modelo}.png') # Abrindo o modelo padrão com o PIL
            merge = Image.new('RGBA', modelo.size) # Abrinda uma nova imagem para edição
            x = int((modelo.size[0]-qrImg.size[0])/2) # Valor Dinamico
            merge.paste(modelo) # Carrega o Modelo
            merge.paste(qrImg, (x, 350)) # Cola o qr code no valor relativo
            txt = Image.open(r'_internal/src/600.png') # Versionamento de texto
            dw = ImageDraw.Draw(txt) # Esrceve a estrutura e centraliza
            fnt = ImageFont.truetype(r'_internal/src/arial_narrow_7.ttf', 35) # Font and size
            x = dw.textlength(self.nomeLocal, fnt) # Aplica os valores
            xt = (600-x)/2 # Valor relativo do Texto
            dw.text((xt, 40), self.nomeLocal, font=fnt, fill='black', align='center') # Fazendo o merge do Texto no modelo com o qrcode
            
            # Salva o arquivo!
            txt.save(r'_internal/src/texto.png')
            imgt = Image.open(r'_internal/src/texto.png')
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
        on('https:  //youtu.be/W6hMMplTn0Q') 
class Login(Screen):
    ... 
class MainWin(Screen):
    ...
class Main(MDApp):
    def build(self):
        super().__init__()
        Builder.load_file('_internal/src/style.kv')
        self.th = self.theme_cls
        self.th.theme_style = 'Dark'
        self.th.primary_palette = 'Gray'
        self.title = 'GeradorQR'
        self.icon = '_internal/src/icon.ico'
        sm = MDScreenManager()
        sm.add_widget(Login())
        sm.add_widget(MainWin())
        return sm

    def on_start(self):
        self.root.current = 'login'
        self.idsMain = self.root.get_screen('mainwin').ids
        self.idsLogin = self.root.get_screen('login').ids
        self.modelo('modeloTrad')
        try:
            g.cons()
            if g.dd != None:
                self.idsLogin.slvUser.active = True
                self.idsLogin.server.text = g.dd[0]
                self.idsLogin.user.text = g.dd[1]
                self.idsLogin.pwd.text = g.dd[2]
        except: ...
            
    def login(self):
        if self.idsLogin.server.text != '' and self.idsLogin.user.text != '' and self.idsLogin.pwd.text != '':
            try:
                if self.idsLogin.slvUser.active: g.ins(uid=self.idsLogin.user.text ,pwd=self.idsLogin.pwd.text , server=self.idsLogin.server.text)
                else: g.excluir()
                g.loginDB(
                    server = self.idsLogin.server.text,
                    uid= self.idsLogin.user.text,
                    pwd= self.idsLogin.pwd.text
                    )
                toast('Logado com Sucesso')
                self.root.current = 'mainwin'
            except: toast('Login Invalido')
        else: toast('Campos Vazios')
        
    def modelo(self, modelo):
        self.md = modelo
        
    def gerar(self):
        try:
            cr = int(self.idsMain.numCR.text)
            nv = int(self.idsMain.numNivel.text)
            if cr != '':
                g.gerar(modelo=self.md, CR=cr, nivel=nv)
                toast(f'QR codes gerados - {g.cr2}')
            else: toast('Valores Invalidos, CR não pode estar em branco')
        except:
            toast('Informações invalidas, digite corretamente')
    def abrirPasta(self):
        g.abrirPastaDeGeracao()
    
    def github(self):
        g.gitHub()
    
    def yt(self):
        g.youtube()

g = Gerador()
Main().run()