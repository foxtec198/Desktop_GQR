from PIL import Image, ImageDraw, ImageFont

def juntar():
    modelo = Image.open('scr/MODELOO.png')
    qr = Image.open('scr/qrteste.png')
    merge = Image.new('RGBA', modelo.size)
    x = int((modelo.size[0]-qr.size[0])/2)
    merge.paste(modelo)
    merge.paste(qr, (x, 300))
    merge.save('teste.png')
    
tt = Image.new('RGBA', (200,100))
d = ImageDraw.Draw(tt)
fnt = ImageFont.truetype('scr/arial_narrow_7.ttf',30)
text = 'TESTE PORTARIA ANALISA'
an = text.split()
an.insert(2, '\n')
d.text((0,0), an, fill='black', font=fnt, align='center')


