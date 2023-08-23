# ===============================================================================
# ===============================================================================
# ===============================================================================
# ========================Criado por Guilherme Breve=============================
# ===============================================================================
# ===============================================================================
# ===============================================================================

import pyodbc as sql # Connect SQL
import yaml as y # Yaml de dados
import segno # Gerador de qr
import os # Sistema
from time import strftime as st # Data e Hora Atual
from PIL import Image, ImageDraw, ImageFont
import PyPDF2 as pdf2
from reportlab.pdfgen import canvas

class gerarQrCodes():
    # Função de inicio
    def __init__(self,  *dd):
        self.user = dd[0]
        self.pasw = dd[1]
        self.estrutura = dd[2]
        self.connect()
        self.definir_estrutura()
        self.logica()
    
    # Puxa os dados de um Yaml Codificado!  
    def yml(self):
        with open('resources/scr/dados.yaml', 'r') as f:
            dict = y.load(f, Loader = y.FullLoader)
            self.server = dict['servidor']
            self.db = dict['db']
            self.db02 = dict['db02']
        
    def definir_estrutura(self):
        self.data = st('%d-%m_%H-%M-%S')
        self.consultaSeparada()
        for i in self.estrutura:self.nomeGrupo=i[2]
        try:
            os.mkdir('resources/QRCodes')
        except:
            pass
        self.nomeDir = f'resources/QRCodes/{self.nomeGrupo}_{self.data}'
        os.makedirs(self.nomeDir)
    
    # Logica para gerar qrcodes
    def logica(self):
        cont = 0
        for c in self.estrutura:
            qrc = c[1] # definindo o qr code
            self.nomeLocal = c[0] # o nome do sublocal
            self.nomeLocal = self.nomeLocal.replace('/','') # removendo barras para n ocasionar erro
            qrcode = segno.make_qr(qrc) # gerando o qrcode.png
            qrLocal = f'{self.nomeDir}/{self.nomeLocal}.png' # definido a estrutura do diretorio
            qrcode.save(qrLocal, scale=10) #salvando o qrcode no diretorio
            qrImg = Image.open(qrLocal) # Abrindo o qrcode com o PIL
            modelo = Image.open('resources/scr/modelo.png') # Abrindo o modelo padrão com o PIL
            merge = Image.new('RGBA', modelo.size) # Abrinda uma nova imagem para edição
            x = int((modelo.size[0]-qrImg.size[0])/2)
            merge.paste(modelo)
            merge.paste(qrImg, (x, 350))
            txt = Image.open('resources/scr/600.png')
            dw = ImageDraw.Draw(txt)
            fnt = ImageFont.truetype('resources/scr/arial_narrow_7.ttf', 35)
            x, y = dw.textsize(self.nomeLocal, fnt)
            xt = (600-x)/2
            dw.text((xt, 40), self.nomeLocal, font=fnt, fill='black', align='center')
            txt.save('resources/scr/texto.png')
            imgt = Image.open('resources/scr/texto.png')
            x = int((modelo.size[0]-imgt.size[0])/2)
            merge.paste(imgt, (x, 200))
            merge.save(qrLocal)
            # trans pdf
            img = Image.open(qrLocal)
            x, y = img.size
            self.nomePdf = f'{self.nomeDir}/{self.nomeLocal}.pdf'
            pdf = canvas.Canvas(self.nomePdf, pagesize=(x, y))
            pdf.drawImage(qrLocal, 0,0)
            pdf.save()
            cont += 1
        self.merge()
        self.remove()
        
    
    def remove(self):
        dir = os.listdir(self.nomeDir)
        for i in dir:
            if '.pdf' in i and i != 'EstruturaCompleta.pdf':
                os.remove(f'{self.nomeDir}/{i}')
            
    def merge(self, *agrs):
        dir = os.listdir(self.nomeDir)
        mg = pdf2.PdfMerger()
        for i in dir:
            if '.pdf' in i:
                with open(f'{self.nomeDir}/{i}', 'rb') as arq:
                    dados = pdf2.PdfReader(arq)
                    mg.append(dados)
        mg.write(f'{self.nomeDir}/EstruturaCompleta.pdf')
        mg.close()
         
    # Conexão com o banco de dados   
    def connect(self):
        # Conecta com o DB
        self.yml()
        st_conn = f"DRIVER=SQL Server; DATABASE={self.db};SERVER={self.server};UID={self.user};PWD={self.pasw}"
        self.conn = sql.connect(st_conn)
        self.c = self.conn.cursor()
        
    def consultaSeparada(self):
        self.cons = f"SELECT Descricao as Nome, QRCode, Grupo FROM Estrutura WHERE HierarquiaDescricao LIKE '%{self.estrutura}%'"
        self.estrutura = self.c.execute(self.cons).fetchall()

        