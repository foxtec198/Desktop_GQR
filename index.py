from PyQt5 import uic, QtWidgets
import main as back
from qdarktheme import setup_theme as set
import os, time
import pyodbc
import sqlite3 as sq

class FrontEnd():
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.loginWin = uic.loadUi('resources/uis/login.ui')
        self.mainWin = uic.loadUi('resources/uis/main.ui')
        self.conn = sq.connect('resources/scr/dd.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS userSalvo(Id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, pasw TEXT, verify INT)")
        set() #seta modo escuro
        
        # Call de funções
        
        # LOGIN
        self.loginWin.btnLogin.clicked.connect(self.main)
        
        # MAIN
        self.mainWin.btnGerarQR.clicked.connect(self.gerarQrCode)
        self.mainWin.btnAbrirPasta.clicked.connect(self.abrirPastaDeGeracao)
        self.estrutura = self.mainWin.estruturaEntry.text
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
        if self.estrutura() != '':
            # try:
            back.gerarQrCodes(self.user, self.pasw, self.estrutura())
            self.msg(self.mainWin, 'Sucesso', 'QRCodes gerados com sucesso')
            # except:
            #     self.msg(self.mainWin, 'Erro', 'Algo deu errado! Confira seu Login')
        else:
            self.msg(self.mainWin, 'Erro!', 'A estrutura não pode estar em branco')
    
    def abrirPastaDeGeracao(self):
        os.system('explorer resources\QRCodes')
    
    def salvarUser(self, *args):
        self.c.execute(f'''
                  INSERT INTO userSalvo(user, pasw, verify)
                  VALUES ('{args[0]}','{args[1]}', 1)
                  ''')
        self.conn.commit()

FrontEnd()