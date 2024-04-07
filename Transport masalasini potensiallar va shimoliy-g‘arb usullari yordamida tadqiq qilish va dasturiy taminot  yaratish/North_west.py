import tkinter as tk
from tkinter import *
from tkinter import ttk
from array import *
import numpy as np



elbek = tk.Tk()
#Dasturning bacground rangi
elbek.configure(background='#edf0ee')
elbek.geometry("930x700")
elbek.title("Transport muammosi")
heading = Label(text = "North West Corner Method - Shimoli-g'arbiy burchak usuli", bg="#154c79", fg = "white", width = "500", height = "1", font=('Arial 22'))
heading.pack()





# scrollbar canvas birinchi sp
frame1 = ttk.Frame(elbek, relief="raised")
frame1.pack(fill=BOTH, side=LEFT)
canvas1 = Canvas(frame1, bg="#edf0ee")
canvas1.pack(side=LEFT, fill=BOTH)
scrolbar1 = ttk.Scrollbar(frame1, orient=VERTICAL, command=canvas1.yview)
scrolbar1.pack(side=RIGHT, fill=Y)
birlashuvchi = Frame(canvas1)
canvas1.create_window((50,10), window=birlashuvchi, anchor="nw")
canvas1.configure(yscrollcommand=scrolbar1.set)
canvas1.bind('<Configure>', lambda e: canvas1.configure(scrollregion = canvas1.bbox("all")))



# scrollbar canvas 2 birlashuvchi 2 dm
frame2 = Frame(elbek, bd=1, relief="raised", bg="#edf0ee")
frame2.pack(fill=BOTH, side=LEFT)
canvas2 = Canvas(frame2, bg="#edf0ee")
canvas2.pack(side=LEFT, fill=BOTH) 
scrolbar2 = ttk.Scrollbar(frame2, orient=VERTICAL, command=canvas2.yview)
scrolbar2.pack(side=RIGHT, fill=Y)
birlashuvchi2 = Frame(canvas2)
canvas2.create_window((50,10), window=birlashuvchi2, anchor="nw")
canvas2.configure(yscrollcommand=scrolbar2.set)
canvas2.bind('<Configure>', lambda e: canvas2.configure(scrollregion = canvas2.bbox("all")))



# scrollbar canvas 3 birlashuvchi 3 matx
frame3 = Frame(elbek, bd=1, relief="raised", bg="#edf0ee")
frame3.pack(fill=BOTH, side=LEFT)
canvas3 = Canvas(frame3, bg="#edf0ee")
canvas3.pack(side=LEFT, fill=BOTH, expand=1) 
scrolbar3 = ttk.Scrollbar(frame3, orient=VERTICAL, command=canvas3.yview)
scrolbar3.pack(side=RIGHT, fill=Y)
birlashuvchi3 = Frame(canvas3)
canvas3.create_window((50,10), window=birlashuvchi3, anchor="nw")
canvas3.configure(yscrollcommand=scrolbar3.set)
canvas3.bind('<Configure>', lambda e: canvas3.configure(scrollregion = canvas3.bbox("all")))






global aaa, bbb, DDD
l1 = 0
l2 = 0
# cretae a.numpy = 
def a_input_function1():
    global l1, a_label, a_input, a
    a_label = Label(birlashuvchi, text=f"A{l1+1}")
    a_label.pack(side=TOP)
    a_input = Entry(birlashuvchi, font = 20, fg = "black", bg="#eeeeee")
    a_input.pack()
    a.append(a_input)
    l1+=1



def a_input_function2():
    global l2, b_input, b
    b_label = Label(birlashuvchi2, text=f"B{l2+1}")
    b_label.pack()
    b_input = Entry(birlashuvchi2, font = 20, fg = "black", bg="#eeeeee")
    b_input.pack()
    b.append(b_input)
    l2+=1


#create matritsa nxm
def a_input_function3():
    global a_1, row, list3
    for i in range(len(a)):
        col = []
        for j in range(len(b)):
            l_1 = Label(birlashuvchi3, text=f"c[{i}][{j}]")
            l_1.pack()
            a_1 = Entry(birlashuvchi3, width="6", fg = "black", bg="#eeeeee")
            a_1.pack()
            col.append(a_1)
        list3.append(col)


a = []
aaa = np.array([])
b = []
bbb = np.array([])
list3 = []
DDD = []


def ekrangaLCM():
    global aaa, bbb, DDD
    for i in range(len(a)):
        intt = int(a[i].get())
        aaa = np.append(aaa, intt)
    for i in range(len(b)):
        intt2 = int(b[i].get())
        bbb = np.append(bbb, intt2)
    for i in list3:
        col2 = []
        for j in i:
            intt3 = int(j.get())
            col2.append(intt3)
        DDD.append(col2)
    NWCM(DDD,bbb,aaa)
    text2 = tk.Text(elbek, width=100, height=100, fg = "black", bg="#eeeeee", font=('Arial 22'),  pady=20)
    text2.pack()
    text2.insert("1.0",NWCM(DDD,bbb,aaa))
    




###------------------North West Corner Method---------------------------
def NWCM(costs, demand, supply):
    a = np.copy(supply)
    b = np.copy(demand)
    c = np.copy(costs)

    if a.sum() != b.sum():
        return 0

    m = len(b)
    n = len(a)
    x = np.zeros((n, m), dtype=np.uint32)

    i = 0
    j = 0
    x_ij = 0
    funk = 0

    while (i < m) and (j <= n):
        x_ij = min(a[i], b[j])
        funk += c[i, j] * x_ij
        a[i] -= x_ij
        b[j] -= x_ij
        x[i, j] = x_ij

        if a[i] > b[j]:
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            i += 1
            j += 1
            
    return x, funk
###---------------------------------------------------------------------


add_label1 = tk.Label(birlashuvchi, text = "Takliflar", font=('Arial 18'))
add_label1.pack(side=tk.TOP)
add_input1 = tk.Button(birlashuvchi, text="+", activeforeground = "green", width=10, font=('Arial 18'), command=a_input_function1)
add_input1.pack(side=tk.TOP)


add_label2 = tk.Label(birlashuvchi2, text = "Talablar", font=('Arial 18'))
add_label2.pack()
add_input2 = tk.Button(birlashuvchi2, text="+", activeforeground = "green", width=10, font=('Arial 18'), command=a_input_function2)
add_input2.pack(side=tk.TOP)


add_label3 = tk.Label(birlashuvchi3, text = "Masala matritsasi", font=('Arial 18'))
add_label3.pack()
add_input3 = tk.Button(birlashuvchi3, text="+", activeforeground = "green", width=10, font=('Arial 18'), command=a_input_function3)
add_input3.pack(side=tk.TOP)


enter2 = tk.Button(birlashuvchi3, text="Yechish", activeforeground = "green", width=10, font=('Arial 18'), command=ekrangaLCM)
enter2.pack(side=tk.TOP)



elbek.mainloop()










