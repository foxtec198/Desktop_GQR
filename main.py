from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from gerador import Gerador
from kivymd.toast import toast

class Login(Screen):
    ... 
class MainWin(Screen):
    ...
class Main(MDApp):
    def build(self):
        Builder.load_file('src/style.kv')
        self.th = self.theme_cls
        self.th.theme_style = 'Dark'
        self.th.primary_palette = 'Gray'
        sm = MDScreenManager()
        sm.add_widget(Login())
        sm.add_widget(MainWin())
        return sm

    def on_start(self):
        self.root.current = 'login'
        self.idsMain = self.root.get_screen('mainwin').ids
        self.idsLogin = self.root.get_screen('login').ids
        self.modelo('modeloTrad')
        g.cons()
        if g.dd != None:
            self.idsLogin.slvUser.active = True
            self.idsLogin.server.text = g.dd[0]
            self.idsLogin.user.text = g.dd[1]
            self.idsLogin.pwd.text = g.dd[2]
        
    def login(self):
        if not self.idsLogin.slvUser.active: g.excluir()
        if self.idsLogin.server.text != '' and self.idsLogin.user.text != '' and self.idsLogin.pwd.text != '':
            try: 
                g.loginDB(
                    server = self.idsLogin.server.text,
                    uid= self.idsLogin.user.text,
                    pwd= self.idsLogin.pwd.text
                    )
                toast('Login Correto')
                self.root.current = 'mainwin'
            except: toast('Login Invalido')
        else: toast('Campos Vazios')
        
    def modelo(self, modelo):
        self.md = modelo
        
    def gerar(self):
        cr = self.idsMain.numCR.text
        nv = self.idsMain.numNivel.text
        if cr != '':
            g.gerar(modelo=self.md, CR=cr, nivel=nv)
            toast(f'QR codes gerados - {g.cr2}')
        else: toast('Valores Invalidos, CR não pode estar em branco')
    
    def abrirPasta(self):
        g.abrirPastaDeGeracao()
    
    def github(self):
        g.gitHub()
    
    def yt(self):
        g.youtube()
       
g = Gerador()
Main().run()