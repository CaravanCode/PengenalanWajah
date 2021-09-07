from tkinter import *
import os
from tkinter import messagebox
import time
from pyfirmata2 import Arduino
import configparser
from pathlib import Path
path = 'training-data'
wajah = 's7'
datWajah = ''

#board = Arduino(Arduino.AUTODETECT)
#pin9 = board.get_pin('d:9:o')


config = configparser.RawConfigParser()
config_path = 'config.txt'
config.read(config_path)
durasi = int(config.get('Config', 'durasi'))

#pin9.write(0)
#print('Tutup')

def get_dir(dir):
    f = open('temp.txt', 'w+')
    f.write(dir)
    f.flush()
    os.fsync(f)


def run():
    os.system('train.py')



main = Tk()
w = 680
h = 560
main.geometry('{}x{}'.format(w,h))
main.wm_title("Face Recognition")
main.resizable(False,False)
canvas = Canvas(main,bg='#20355e', width=680,height=560)
canvas.pack()
inst = Label(canvas, text="Silahkan input nama direktori baru lalu tekan 'Record'", bg='#20355e', fg='#07ef2a')
inst.pack()
inst.place(x=200,y=380)


svalue = StringVar() # defines the widget state as string
widgeth = Label(canvas)
widgeth.pack()
widgeth.place(x=140,y=130)
frameCnt = 46
frames = [PhotoImage(file='bg3.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    widgeth.configure(image=frame)
    main.after(100, update, ind)



main.after(0, update, 0)


comments = """Dibuat oleh Regiyan Irvan
"""

widgets = Label(main,text=comments, bg='#20355e', fg='white')
widgets.pack()
widgets.place(x=530,y=520)

w = Entry(main,textvariable=svalue, width = 40) # adds a textarea widget
w.pack()
w.place(x=220,y=400)

img = PhotoImage(file= 'title4.png')
title = Label(canvas, image = img, border= 0)
title.pack()
title.place(x=60,y=20)

def MakeDir(dir):
    MsgBox = messagebox.askquestion ('Buat direktori baru','Apakah anda yakin ingin membuat direktori baru?',icon = 'warning')
    if MsgBox == 'yes':
        os.mkdir(dir)
        print("Direktori berhasil dibuat")
        messagebox.showinfo('Berhasil', 'Direktori berhasil dibuat')
        get_dir(dir)
        MsgBox_train = messagebox.askquestion('Buat training baru', 'Mulai merekam?', icon='warning')
        if MsgBox_train == 'yes':
            run()

def eigen_train_button_fn():
    name = svalue.get()
    #os.system('python train_eigen.py %s'%name)
    #os.system('train.py')

    if name=='':
        messagebox.showerror('Error','Nama direktori tidak boleh kosong jika anda ingin membuat direktori baru')
    else:
        print(name)
        wajah = name
        print(path+'/'+wajah)
        check_dir(wajah)




def eigen_recog_button_fn():
    os.system('recognition.py')


def prepare_eigen_button_fn():
    os.system('prepare_train.py')


def check_dir(dir):
    isdir = os.path.isdir(path + '/' + dir)
    if isdir is True:
        print(isdir)
        messagebox.showinfo('Peringatan','Direktori sudah ada')
    else:
        print("Tidak ada")
        MakeDir(path + '/' + dir)
    return isdir

'''
def door():
    pin9.write(1)
    print('Buka')
    time.sleep(durasi)
    pin9.write(0)
    print('Tutup')
'''

train_eigen_button = Button(main,text="Record", command=(lambda:eigen_train_button_fn()), width=10, height=2, bg='#147f4d', activebackground='#1a7ace',fg='white')
train_eigen_button.pack()
train_eigen_button.place(x=300,y=430)
recog_eigen_button = Button(main,text="Recognize", command=(lambda: eigen_recog_button_fn()), width=10, height=2, bg='#147f4d', activebackground='#1a7ace',fg='white')
recog_eigen_button.pack()
recog_eigen_button.place(x=400,y=430)
prepare_eigen_button = Button(canvas,text="Train", command=(lambda: prepare_eigen_button_fn()), width=10, height=2, bg='#147f4d', activebackground='#1a7ace',fg='white')
prepare_eigen_button.pack()
prepare_eigen_button.place(x=200,y=430)
#door_open_button = Button(canvas,text="Buka", command=(lambda: door()), width=10, height=2, bg='#147f4d', activebackground='#1a7ace',fg='white')
#door_open_button.pack()
#door_open_button.place(x=30,y=500)
main.mainloop()



