from win10toast import ToastNotifier

n = ToastNotifier()
n.show_toast(
    'Teste de Notify',
    'Gerando qr codes',
    duration=10,
    icon_path="resources/scr/icon.ico"
)