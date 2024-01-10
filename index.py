from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import Screen
from kivy.lang import Builder

class Login(Screen):
    ...
    
class MainWin(Screen):
    ...
    
class Main(MDApp):
    def build(self):
        super().__init__()
        Builder.load_file('src/style.kv')
        th = self.theme_cls
        th.thme_style = 'Dark'
        sm = MDScreenManager()
        sm.add_widget(Login())
        sm.add_widget(MainWin())
        return sm

    def on_start(self):
        self.root.current = 'login'
    
if __name__ == '__main__':
    Main().run()