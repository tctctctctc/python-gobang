#encoding:utf-8
from Tkinter import *

def fun():

top = Tk()
top.title('IP')
top.geometry('300x200')

L1 = Label(top,text='     IP 地址:',font='宋体',padx=5,pady=30)
L1.grid(row=1,column=0)
E1 = Entry(top,font='华文行楷')
E1.grid(row=1,column=1)
mainloop()