from os import system, makedirs, mkdir, remove, listdir 
from pyodbc import connect as sql# Connect SQL
from yaml import load, FullLoader# Yaml de dados
from segno import make_qr # Gerador de qr
from time import strftime as st # Data e Hora Atual
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfReader, PdfMerger
from reportlab.pdfgen import canvas
from PyQt5 import uic, QtWidgets as qw
from qdarktheme import setup_theme as set
from webbrowser import open_new_tab as on
from sqlite3 import connect

class GeradorQR():
    def run(self):
        self.app = qw.QApplication([])
        
        self.main = uic.loadUi('resources/uis/main.ui')
        self.login = uic.loadUi('resources/uis/login.ui')
        set()
        self.connL = connect('resources/scr/dd.db')
        self.c = self.connL.cursor()
        
        self.login.btnLogin.clicked.connect(self.realizarLogin)
        
        self.main.btnGerarQR.clicked.connect(self.validar)
        self.main.btnAbrirPasta.clicked.connect(self.abrirPastaDeGeracao)
        self.main.gitBtn.clicked.connect(self.gitHub)
        
        u = self.c.execute('SELECT * FROM USERS ORDER BY Id DESC').fetchone()
        if u != None:
            Id = [0]
            self.action(f'DELETE FROM USERS WHERE Id <> "{Id}"')
            self.login.entryServer.setText(u[3])
            self.login.entryUser.setText(u[1])
            self.login.entryPasw.setText(u[2])
            self.login.saveUser.setChecked(True)
        self.login.show()
        
        self.app.exec()

    def realizarLogin(self):
        self.server = self.login.entryServer.text()
        self.user = self.login.entryUser.text()
        self.pwd = self.login.entryPasw.text()
        nome = self.user.replace('.', ' ')
        nome = nome.split()
        
        if self.login.saveUser.isChecked():
            self.action(f"INSERT INTO USERS(user, pwd, servidor)VALUES('{self.user}','{self.pwd}','{self.server}')")
        else:
            self.action(f'DELETE FROM USERS')
        
        try:
            self.conn = sql(f"DRIVER=SQL Server;SERVER={self.server};UID={self.user};PWD={self.pwd}")
            self.c2 = self.conn.cursor()
            self.msg(self.login, 'Logado com Sucesso!', f'Logado com sucesso, bem vindo {nome[0]}')
            self.main.show()
            self.login.close()
        except:
            self.msg(self.login, 'Erro de Login!','Confirme o VPN e/ou suas Credenciais!!! ')
    
    def validar(self):
        ...
    def gerar(self):
        ForceRadio = self.main.ForceRadio
        MiniRadio = self.main.MiniRadio
        OnSegRadio = self.main.OnSegRadio
        PoliRadio = self.main.PoliRadio
        TopRadio = self.main.TopRadio
        TradRadio = self.main.TradRadio
        
        if ForceRadio.isChecked(): self.modelo = 'modeloForce'
        if MiniRadio.isChecked(): self.modelo = 'modeloMini'
        if OnSegRadio.isChecked(): self.modelo = 'modeloOnSeg'
        if PoliRadio.isChecked(): self.modelo = 'modeloPoli'
        if TopRadio.isChecked(): self.modelo = 'modeloTop'
        if TradRadio.isChecked(): self.modelo = 'modeloTrad'
        
        
        
    def abrirPastaDeGeracao(self):
        system('Explorer resources\QRCodes')
        
    def gitHub(self):
        on('https://github.com/foxtec198/GeradorQR/issues/new')
    
    def action(self, consulta):
        self.c.execute(consulta)
        self.connL.commit()
         
    def msg(self, win, title, text):
        qw.QMessageBox.about(win, title, text)
        
    
GeradorQR().run()