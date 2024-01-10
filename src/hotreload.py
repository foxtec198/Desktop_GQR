from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder

class Login(Screen):
    ...
    
class MainWin(Screen):
    ...
    
class Main(MDApp):
    DEBUG = True
    KV_FILES = ['src/style.kv']
    
    def build_app(self):
        Builder.load_file('src/style.kv')
        th = self.theme_cls
        th.theme_style = 'Dark'
        th.primary_palette = "Gray"
        sm = MDScreenManager()
        sm.add_widget(Login())
        # sm.add_widget(MainWin())
        return sm
        
Main().run()