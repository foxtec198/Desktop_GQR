#; ===============================================================================
# ===============================================================================
# ===============================================================================
# ========================Criado por Guilherme Breve=============================
# ===============================================================================
# ===============================================================================
# ===============================================================================

from sys import exit
from os import system, makedirs, mkdir, remove, listdir 
from pyodbc import connect as sql# Connect SQL
from yaml import load, FullLoader# Yaml de dados
from segno import make_qr # Gerador de qr
from time import strftime as st # Data e Hora Atual
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfReader, PdfMerger
from reportlab.pdfgen import canvas
from PyQt5 import uic, QtWidgets
from qdarktheme import setup_theme as set
from webbrowser import open_new_tab as on
from sqlite3 import connect

class App():
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.loginWin = uic.loadUi('resources/uis/login.ui')
        self.mainWin = uic.loadUi('resources/uis/main.ui')
        self.conn = connect('resources/scr/dd.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS userSalvo(Id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, pasw TEXT, verify INT)")
        set() #seta modo escuro 
        
        # Call de funções
        # LOGIN
        self.loginWin.btnLogin.clicked.connect(self.main)
        
        # MAIN
        self.mainWin.btnGerarQR.clicked.connect(self.gerarQrCode)
        self.mainWin.btnAbrirPasta.clicked.connect(self.abrirPastaDeGeracao)
        self.mainWin.gitBtn.clicked.connect(self.gitHub)
        self.loginWin.show()
        
        # Verifica se o login foi salvo
        u = self.c.execute('select user, pasw, verify from userSalvo ORDER BY Id DESC').fetchone()
        if u != None:#Confere se não está vazio
            UltimoId = self.c.execute('select Id from userSalvo order by Id desc').fetchone()[0]
            self.c.execute(f"delete from userSalvo where Id <> '{UltimoId}' ")
            if u[2] == 1:
                #Realiza o preenchimento
                self.loginWin.entryUser.setText(u[0])
                self.loginWin.entryPasw.setText(u[1])
                self.loginWin.saveUser.setChecked(True)
        self.app.exec()
        
    def msg(self, *args):
        # WIN - TITULO - MENSAGEM 
        QtWidgets.QMessageBox.about(args[0], args[1], args[2])
    
    def gitHub(self):
        on('https://github.com/foxtec198/GeradorQR/issues/new')
        
    def main(self):
        self.user = self.loginWin.entryUser.text()
        self.pasw = self.loginWin.entryPasw.text()
        if self.loginWin.saveUser.isChecked():
            self.salvarUser(self.user, self.pasw)
        else:
            self.c.execute('delete from userSalvo')
            self.conn.commit()
            
        if self.user != '' and self.pasw != '':
            try:
                self.loginWin.close()
                self.mainWin.show()
            except:
                self.msg(self.loginWin, 'Erro de Login', 'Dados Incorretos // VPN não Ativo')
        else:
            self.msg(self.loginWin, 'Erro!', 'Os dados de login não\npode estar em branco !!!')
            
    def gerarQrCode(self):
        self.estrutura = self.mainWin.estruturaEntry.text
        if self.estrutura() != '':
            self.msg(self.mainWin, 'Sucesso', 'Gerando QR Codes...')
            self.exec(self.user, self.pasw, self.estrutura())
            self.msg(self.mainWin, 'Sucesso', f'QRCodes gerados com sucesso - {self.nomeDir}')
        elif self.estrutura() == '':
            self.msg(self.mainWin, 'Erro!', 'A estrutura não pode estar em branco')
        else:
            self.msg(self.mainWin, 'Erro!', 'Algo deu errado confira o Login!')
            
    
    def abrirPastaDeGeracao(self):
        system('explorer resources\QRCodes')
    
    def salvarUser(self, *args):
        self.c.execute(f'''
                  INSERT INTO userSalvo(user, pasw, verify)
                  VALUES ('{args[0]}','{args[1]}', 1)
                  ''')
        self.conn.commit()
        
    def exec(self, *dd):
        self.user = dd[0]
        self.pasw = dd[1]
        self.estrutura = dd[2]
        self.connect()
        self.definir_estrutura()
        self.logica()
        
    # Puxa os dados de um Yaml Codificado!  
    def yml(self):
        with open('resources/scr/dados.yaml', 'r') as f:
            dict = load(f, Loader = FullLoader)
            self.server = dict['servidor']
            self.db = dict['db']
            self.db02 = dict['db02']
    
    def modeloQR(self):
        ForceRadio = self.mainWin.ForceRadio
        MiniRadio = self.mainWin.MiniRadio
        OnSegRadio = self.mainWin.OnSegRadio
        PoliRadio = self.mainWin.PoliRadio
        TopRadio = self.mainWin.TopRadio
        TradRadio = self.mainWin.TradRadio
        imgLbl = self.mainWin.imgLbl
        
        if ForceRadio.isChecked(): self.modelo = 'modeloForce'
        if MiniRadio.isChecked(): self.modelo = 'modeloMini'
        if OnSegRadio.isChecked(): self.modelo = 'modeloOnSeg'
        if PoliRadio.isChecked(): self.modelo = 'modeloPoli'
        if TopRadio.isChecked(): self.modelo = 'modeloTop'
        if TradRadio.isChecked(): self.modelo = 'modeloTrad'
        
    def definir_estrutura(self):
        self.data = st('%d-%m_%H-%M-%S')
        self.consultaSeparada()
        for i in self.estrutura:self.nomeGrupo=i[2]
        try:
            mkdir('resources/QRCodes')
        except:
            pass
        self.nomeDir = f'resources/QRCodes/{self.nomeGrupo}_{self.data}'
        makedirs(self.nomeDir)
        
    def logica(self):
        self.modeloQR()
        print(self.modelo)
        cont = 0
        for c in self.estrutura:
            qrc = c[1] # definindo o qr code
            self.nomeLocal = c[0] # o nome do sublocal
            self.nomeLocal = self.nomeLocal.replace('/','') # removendo barras para n ocasionar erro
            qrcode = make_qr(qrc) # gerando o qrcode.png
            qrLocal = f'{self.nomeDir}/{self.nomeLocal}.png' # definido a estrutura do diretorio
            qrcode.save(qrLocal, scale=10) #salvando o qrcode no diretorio
            qrImg = Image.open(qrLocal) # Abrindo o qrcode com o PIL
            modelo = Image.open(f'resources/scr/{self.modelo}.png') # Abrindo o modelo padrão com o PIL
            merge = Image.new('RGBA', modelo.size) # Abrinda uma nova imagem para edição
            x = int((modelo.size[0]-qrImg.size[0])/2) # Valor Dinamico
            merge.paste(modelo) # Carrega o Modelo
            merge.paste(qrImg, (x, 350)) # Cola o qr code no valor relativo
            txt = Image.open('resources/scr/600.png') # Versionamento de texto
            dw = ImageDraw.Draw(txt) # Escreve a estrutura e centraliza
            fnt = ImageFont.truetype('resources/scr/arial_narrow_7.ttf', 35) # Font and size
            x, y = dw.textsize(self.nomeLocal, fnt) # Aplica os valores
            xt = (600-x)/2 # Valor relativo do Texto
            dw.text((xt, 40), self.nomeLocal, font=fnt, fill='black', align='center') # Fazendo o merge do Texto no modelo com o qrcode
            
            # Salva o arquivo!
            txt.save('resources/scr/texto.png')
            imgt = Image.open('resources/scr/texto.png')
            x = int((modelo.size[0]-imgt.size[0])/2)
            merge.paste(imgt, (x, 200))
            merge.save(qrLocal)
            
            # Transforma o arquivo em pdf com todos os QRs
            img = Image.open(qrLocal)
            x, y = img.size
            self.nomePdf = f'{self.nomeDir}/{self.nomeLocal}.pdf'
            pdf = canvas.Canvas(self.nomePdf, pagesize=(x, y))
            pdf.drawImage(qrLocal, 0,0)
            pdf.save()
            cont += 1
            
        self.merge()
        self.remove()
        # exit()
        
    def remove(self):
        dir = listdir(self.nomeDir)
        for i in dir:
            if '.pdf' in i and i != 'EstruturaCompleta.pdf':
                remove(f'{self.nomeDir}/{i}')
            
    def merge(self, *agrs):
        dir = listdir(self.nomeDir)
        mg = PdfMerger()
        for i in dir:
            if '.pdf' in i:
                with open(f'{self.nomeDir}/{i}', 'rb') as arq:
                    dados = PdfReader(arq)
                    mg.append(dados)
        mg.write(f'{self.nomeDir}/EstruturaCompleta.pdf')
        mg.close()
         
    # Conexão com o Banco de Dados   
    def connect(self):
        # Conecta com o DB
        self.yml()
        st_conn = f"DRIVER=SQL Server; DATABASE={self.db};SERVER={self.server};UID={self.user};PWD={self.pasw}"
        self.conn = sql(st_conn)
        self.c = self.conn.cursor()
        
    def consultaSeparada(self):
        self.cons = f"SELECT Descricao as Nome, QRCode, Grupo FROM Estrutura WHERE HierarquiaDescricao LIKE '%{self.estrutura}%'"
        self.estrutura = self.c.execute(self.cons).fetchall()
        
        
App()