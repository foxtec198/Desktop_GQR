from PIL import Image, ImageDraw, ImageFont

text = 'CHORRASCARIA'
qr = Image.open('scr/qrteste.png')

modelo = Image.open('scr/MODELOO.png')
merge = Image.new('RGBA', modelo.size)
x = int((modelo.size[0]-qr.size[0])/2)
merge.paste(modelo)
merge.paste(qr, (x, 300))
merge.save('teste.png')

textoImg = Image.open('scr/blank.png')
addText = ImageDraw.Draw(textoImg)
fonte = ImageFont.truetype('scr/arial_narrow_7.ttf', 50)
addText.text((0,30), text, fill='Black', font=fonte)
x2 = int((modelo.size[0]-textoImg.size[0])/2)
merge.paste(textoImg, (x2, 200))
merge.show()
print(qr.size[0])

