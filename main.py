from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from qdarktheme import setup_theme
from sys import argv, exit
from qrcode import QRCode
from models.notify import Notify
from models.version import Version
from sqlite3 import connect
from os import system
from functools import cache
from datetime import datetime as dt
from webbrowser import open_new_tab

qr = QRCode()
app = QApplication(argv)

class GQR:
    def __init__(self):
        self.conn = connect('src/db/temp.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS "user" (
        "server" TEXT,
        "user"	 TEXT,
        "pwd"	 TEXT)
        """)
        setup_theme('dark')
        self.win = loadUi('src/ui/main.ui')
        self.callbacks()
        self.confirmar_dados()
        self.win.pages.setCurrentWidget(self.win.login)
        self.win.nivel.setCurrentText('3 - CR')
        self.pg = self.win.pg
        self.win.fmPg.hide()
        version = Version().get_version()
        self.win.credits.setText(f'Desenvolvido por tecnobreve 2024 © - Versão: {version}')
        self.win.show()
        exit(app.exec_())
    
    def msg(self, msg):
        QMessageBox.about(self.win, 'Gerador QR', msg)

    def callbacks(self):
        # self.win.btnLogin.clicked.connect(lambda: Thread(target=self.connect).start())
        self.win.btnLogin.clicked.connect(self.connect)
        self.win.btnGerar.clicked.connect(self.gerar)
        self.win.btnPasta.clicked.connect(self.abrir_pasta)

        self.win.btnGit.clicked.connect(self.abrir_github)
        self.win.btnYt.clicked.connect(self.abrir_youtube)
        self.win.btnDocs.clicked.connect(self.abrir_docs)
        self.win.btnTelegram.clicked.connect(self.abrir_telegram)

    def add_value(self, x):
        self.pg.setValue(x)

    # Functions
    def confirmar_dados(self):
        user = self.win.user.text()
        pwd = self.win.pwd.text()
        server = self.win.server.text()
        slv = self.win.salvar.isChecked()

        self.c.execute('SELECT * FROM user')
        dbu = self.c.fetchone()
        
        if dbu:
            self.win.user.setText(dbu[1])
            self.win.pwd.setText(dbu[2])
            self.win.server.setText(dbu[0])
            self.win.salvar.setChecked(True)
            self.c.execute(f'UPDATE user SET user="{dbu[1]}", pwd="{dbu[2]}", server="{dbu[0]}"')
            self.conn.commit()

        # if dbu and not slv:
        #     self.c.execute('DELETE FROM user')
        #     self.conn.commit()

        elif not dbu and slv:
            if user and pwd and server:
                self.c.execute(f'INSERT INTO user(user, pwd, server) VALUES ("{user}","{pwd}","{server}");')
                self.conn.commit()

    def connect(self):
        user = self.win.user.text()
        pwd = self.win.pwd.text()
        server = self.win.server.text()

        self.win.fmPg.show()
        self.add_value(0)
        self.confirmar_dados()

        self.add_value(10)
        res = qr.new_connect_db(user, pwd, server)
        print(res)
        if res == 'Conectado':
            self.add_value(20)
            self.crs()
            self.win.fmPg.hide()
            self.win.cr.currentTextChanged.connect(lambda x: self.mudar_template(x))
            self.win.username.setText(user)
            self.win.dateuser.setText(dt.now().strftime('Login: %d/%m/%Y %H:%M'))
            self.win.pages.setCurrentWidget(self.win.main)
        else: 
            self.win.fmPg.hide()
            self.msg(res)

    def abrir_pasta(self):
        system("CD QRCodes && explorer .")

    def crs(self):
        crs = qr.cons_crs()
        self.add_value(30)

        self.win.cr.clear()
        for i in crs:
            self.win.cr.addItem(i)
        self.add_value(40)
    
    @cache
    def mudar_template(self, cr):
        if ' - POR - ' in cr: tmp = 'src/cores/modeloAzulEscuro.png'
        elif ' - MAV - ' in cr: tmp = 'src/cores/modeloVerde.png'
        elif ' - MAP -' in cr: tmp = 'src/cores/modeloVermelho.png'
        elif ' - LPG -' in cr: tmp = 'src/cores/modeloAzul.png'
        elif ' - SEG -' in cr: tmp = 'src/cores/modeloAzulEscuro.png'
        else: tmp = 'src/cores/modeloCinza.png'
        self.win.qr.setIcon(QIcon(tmp))

    def gerar(self):
        self.win.fmPg.show()
        self.add_value(10)
        cr = self.win.cr.currentText()
        self.add_value(20)
        op_nivel = self.win.op_nivel.currentText()
        self.add_value(30)
        nivel = self.win.nivel.currentText()
        self.add_value(40)
        empresa = self.win.empresa.currentText()
        self.add_value(50)
        tipo = self.win.tipo.currentText()
        self.add_value(60)
        print(cr, '=', nivel, op_nivel, empresa, tipo)
        res = qr.gerar(cr, '=', nivel, op_nivel, empresa, tipo)
        Notify()
        self.add_value(100)
        self.msg(res)
        self.win.fmPg.hide()   

    def abrir_youtube(self):
        open_new_tab('https://www.youtube.com/watch?v=W6hMMplTn0Q&t=15s')

    def abrir_telegram(self):
        open_new_tab('https://t.me/gps_cns_bot')

    def abrir_docs(self):
        open_new_tab('https://desktop-gqr.readthedocs.io/en/latest/#como-gerar')

    def abrir_github(self):
        open_new_tab('https://github.com/foxtec198/Desktop_GQR')

GQR()