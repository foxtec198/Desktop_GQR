from winotify import Notification, audio

class Notify:
    def __init__(self):
        nt = Notification(
            app_id="Gerador QR", 
            title='QR Code Gerados!!!!!', 
            msg=f'Pronto! Agora basta abrir a pasta de exportação e imprimir ou compartilhar.',
            duration='long',
            )
        # nt.set_audio(audio.LoopingAlarm10, loop=True)
        nt.add_actions(label='Feito!')
        nt.show()

if __name__ == '__main__':
    Notify()