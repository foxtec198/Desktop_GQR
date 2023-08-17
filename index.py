from PyQt5 import uic, QtWidgets
import main as back
from qdarktheme import setup_theme as set
import os

class FrontEnd():
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.loginWin = uic.loadUi('uis/login.ui')
        self.mainWin = uic.loadUi('uis/main.ui')
        set()
        
        # Call de funções
        # LOGIN
        self.loginWin.btnLogin.clicked.connect(self.main)
        self.radioBtn = self.loginWin.radioSaveUser
        # MAIN
        self.mainWin.btnGerarQR.clicked.connect(self.gerarQrCode)
        self.mainWin.btnAbrirPasta.clicked.connect(self.abrirPastaDeGeracao)
        self.estrutura = self.mainWin.estruturaEntry.text
        self.loginWin.show()
        self.app.exec()
        
    def msg(self, *args):
        # WIN - TITULO - MENSAGEM 
        QtWidgets.QMessageBox.about(args[0], args[1], args[2])
         
    def main(self):
        self.user = self.loginWin.entryUser.text()
        self.pasw = self.loginWin.entryPasw.text()
        if self.user != '' and self.pasw != '':
            try:
                self.loginWin.close()
                self.mainWin.show()
            except:
                self.msg(self.loginWin, 'Erro de Login', 'Dados Incorretos // VPN não Ativo')
        else:
            self.msg(self.loginWin, 'Erro!', 'Login não pode estar em branco')
            
    def gerarQrCode(self):
        if self.estrutura() != '':
            back.gerarQrCodes(self.user, self.pasw, self.estrutura())
            self.msg(self.mainWin, 'Sucesso', 'QRCodes gerados com sucesso')
        else:
            self.msg(self.mainWin, 'Erro!', 'A estrutura não pode estar em branco')
    
    def abrirPastaDeGeracao(self):
        os.system('explorer QRCodes')
        
FrontEnd()