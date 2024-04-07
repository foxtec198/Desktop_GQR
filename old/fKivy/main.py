# imports Front
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.toast import toast
from models.back import *

class Login(Screen): ... 
class MainWin(Screen): ...

class Main(MDApp):
    def build(self):
        super().__init__()
        Builder.load_file('src/style.kv')
        self.th = self.theme_cls
        self.th.theme_style = 'Dark'
        self.th.primary_palette = 'Gray'
        self.title = 'GeradorQR'
        self.icon = 'src/icon.ico'
        sm = MDScreenManager()
        sm.add_widget(Login())
        sm.add_widget(MainWin())
        return sm

    def on_start(self):
        self.root.current = 'login'
        self.idsMain = self.root.get_screen('mainwin').ids
        self.idsLogin = self.root.get_screen('login').ids
        self.modelo('modeloTrad')
        b.cons()
        try:
            if b.dd != None:
                self.idsLogin.slvUser.active = True
                self.idsLogin.serverLogin.text = b.dd[0]
                self.idsLogin.uidLogin.text = b.dd[1]
                self.idsLogin.pwdLogin.text = b.dd[2]
        except: ...
            
    def login(self, *args):
        lg = b.login_sql(args[0], args[1], args[2])
        if lg == 'Logado com Sucesso': 
            self.root.current = 'mainwin'
            if self.idsLogin.slvUser.active: b.ins(args[0], args[1], args[2])
            toast(lg)
        else: toast(lg)
        
    def modelo(self, modelo):
        self.md = modelo
        
    def gerar(self, cr, nv):
        qr = QRCode().gerar_qr(self.md, cr, nv)
        if qr not in 'QRCodes gerados com sucesso': toast(qr)

    def abrirPasta(self):
        b.abrir_pasta_de_geração()
    
    def github(self):
        b.abrir_gitHub()
    
    def yt(self):
        b.abrir_youtube()

b = BackEnd()
Main().run()