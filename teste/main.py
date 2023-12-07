from tkinter import Tk, Button

def trocar():
    win2 = Tk()
    win.destroy()
    
win  = Tk()

btn = Button(
    text='Teste',
    font='Arial 20 bold',
    command = trocar
)

btn.pack()
win.mainloop()