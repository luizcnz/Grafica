# Examen.py

import tkinter as tk
import os
from tkinter.constants import RIGHT, TOP, X
import tkinter.font as TkFont
from tkinter import ttk
import time
import tkinter.messagebox as MessageBox
import tkinter.scrolledtext as ScrolledText

import subprocess
import time

ventana = tk.Tk()
ventana.geometry("1250x750")
ventana.title("Peajes")

# Configuracion de texto
texto=TkFont.Font(family="Calibri bold italic",size=14)
textoEtiqueta= TkFont.Font(family="Calibri italic",size=14)
textobotones=TkFont.Font(family="Calibri italic",size=12)


Label_Titulo=tk.Label(ventana,text="Cobro de Peaje",font=texto).place(relx=0.01, rely=0.01, relheight=0.05, relwidth=1)

#----------------------------------CONTENEDOR*------------------------------------------
marcoCentral= tk.Frame(ventana,bg="#E3E1E1",width=1250,height=750)
marcoCentral.pack(padx=10,pady=50,anchor="nw")

#------------------LABEl UBICACION-------------------

lblPlaca=tk.Label(marcoCentral,text="Ubicacion del Peaje ",font=textoEtiqueta,bg="#E3E1E1") .place(x=50, y=20)
cmbUbication=ttk.Combobox(marcoCentral,width=30, values=["Marcovia","Choluteca","San Lorenzo"]).place(x=220, y=25)



#------------------------------------IMAGEN DEL CARRO----------------------------------
auto = tk.PhotoImage(file="Fotos/auto1.png")
panel = tk.Label(marcoCentral, image = auto, width=600,height=500).place(x=10,y=70)

lblPlaca=tk.Label(marcoCentral,text="Numero de Placa Detectado: ",font=textoEtiqueta,bg="#E3E1E1") .place(x=30,y=590)

txtPlaca=tk.Entry(marcoCentral,width=30,justify=tk.RIGHT).place(x=270,y=595)

imgSearch=tk.PhotoImage(file="iconos/buscar32.png")
btnSearch=tk.Button(marcoCentral,image=imgSearch,text=" Buscar ", font=textobotones,compound="left").place(x=480,y=585)

#EL place la X se mueve para de izquierda a derecha
imgTicket=tk.PhotoImage(file="iconos/boleto32.png")
btnTicket=tk.Button(marcoCentral,image=imgTicket,text=" Ticket ", font=textobotones,compound="left").place(x=700,y=150)

imgFactura=tk.PhotoImage(file="iconos/cuenta32.png")
btnFactura=tk.Button(marcoCentral,image=imgFactura,text=" Factura ", font=textobotones,compound="left").place(x=700,y=250)



imgRefresh=tk.PhotoImage(file="iconos/recargar.png")
btnRefresh=tk.Button(marcoCentral,image=imgRefresh,text=" Nuevo ", font=textobotones,compound="left").place(x=700,y=450)




ventana.mainloop()