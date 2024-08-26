from os import system
from shutil import copytree, rmtree

with open('version') as v: oldVersion = v.read() # Pega a versão atual

system('cls') # Limpa a tela
print('Versão antiga: ' + oldVersion)

newVersion = input('Nova versão: ') # Nova versão
if newVersion == '': newVersion = oldVersion

# Muda a versão do ISS
with open('src/instalador.iss', 'r') as file:
    txt = file.read()
    txtNovo = txt.replace(f'#define MyAppVersion "{oldVersion}"', f'#define MyAppVersion "{newVersion}"')
with open('src/instalador.iss', 'w') as file:
    file.write(txtNovo)

# Muda o arquivo local!
with open('version', 'w') as file:
    file.write(newVersion)

# Gera o Executavel
system(""" pyinstaller --noconfirm --onedir --windowed --icon "C:/Users/Guilherme Breve/Documents/GitHub/Desktop_GQR/src/favicon.ico" --name "Gerador QR" --log-level "ERROR" --add-binary "C:/Users/Guilherme Breve/Documents/GitHub/Desktop_GQR/qrcode.py;." --add-binary "C:/Users/Guilherme Breve/Documents/GitHub/Desktop_GQR/models/notify.py;." --add-binary "C:/Users/Guilherme Breve/Documents/GitHub/Desktop_GQR/models/version.py;."  "C:/Users/Guilherme Breve/Documents/GitHub/Desktop_GQR/main.py" """)
# system('pyinstaller instalador.spec')

copytree('src', r'build/Gerador QR/src')

# Abre o arquivo ISS
system('cd src && instalador.iss')
input('Atualizado com sucesso!')