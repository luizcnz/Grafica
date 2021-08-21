# Examen.py

import tkinter as tk
import os
from tkinter.constants import RIGHT, TOP, X
import tkinter.font as TkFont
from tkinter import Frame, Label, ttk
import time
import tkinter.messagebox as MessageBox
import tkinter.scrolledtext as ScrolledText

import subprocess
import time

ventana = tk.Tk()
ventana.geometry("1250x750")
ventana.title("Peajes")
ventana.resizable(0,0)

# Configuracion de texto
texto=TkFont.Font(family="Calibri bold italic",size=14)
textoEtiqueta= TkFont.Font(family="Calibri italic",size=14)
textobotones=TkFont.Font(family="Calibri italic",size=12)
textoEnunciado=TkFont.Font(family="Calibri bold italic",size=12)
textoResultado=TkFont.Font(family="Calibri italic",size=12)

Label_Titulo=tk.Label(ventana,text="Cobro de Peaje",font=texto).place(relx=0.01, rely=0.01, relheight=0.05, relwidth=1)

#----------------------------------CONTENEDOR*------------------------------------------
marcoCentral= tk.Frame(ventana,bg="#E3E1E1").place(relx=0.01, rely=0.06,relheight=0.90, relwidth=0.98)


#------------------LABEl UBICACION-------------------

lblPlaca=tk.Label(marcoCentral,text="Ubicacion del Peaje ",font=textoEtiqueta,bg="#E3E1E1") .place(relx=0.02, rely=0.11)
cmbUbication=ttk.Combobox(marcoCentral,width=30, values=["Marcovia","Choluteca","San Lorenzo"]).place(relx=0.15, rely=0.12)



#------------------------------------IMAGEN DEL CARRO----------------------------------
auto = tk.PhotoImage(file="Fotos/auto1.png")
panel = tk.Label(marcoCentral, image = auto, width=600,height=500).place(relx=0.02, rely=0.18)


#------------------------------------LABEL FINAL----------------------------------
lblPlaca=tk.Label(marcoCentral,text="Numero de Placa Detectado: ",font=textoEtiqueta,bg="#E3E1E1").place(relx=0.02, rely=0.88)

txtPlaca=tk.Entry(marcoCentral,width=30,justify=tk.RIGHT).place(relx=0.22, rely=0.89)

imgSearch=tk.PhotoImage(file="iconos/buscar32.png")
btnSearch=tk.Button(marcoCentral,image=imgSearch,text=" Buscar ", font=textobotones,compound="left").place(relx=0.38, rely=0.88)

#------------------------------------REPORTE -------------------------------------------------------
frameReport = Frame()
frameReport.place(relx=0.51, rely=0.18,relheight=0.30, relwidth=0.47)
frameReport.config(bg="#CFCFCF")
lblOwner= Label(frameReport,text="Titular del Vehiculo: ",font=textoEnunciado, bg="#CFCFCF").place(relx=0.01, rely=0.03)
lblOwnerResult= Label(frameReport,text="Prueba ",font=textoResultado, bg="#CFCFCF").place(relx=0.30, rely=0.03)

lblUbication= Label(frameReport,text="Ubicacion: ",font=textoEnunciado, bg="#CFCFCF").place(relx=0.70, rely=0.03)
lblUbicationResult= Label(frameReport,text="SPS ",font=textoResultado, bg="#CFCFCF").place(relx=0.85, rely=0.03)

lblReport= Label(frameReport,text="Reporte: ",font=textoEnunciado, bg="#CFCFCF").place(relx=0.01, rely=0.17)
lblReportResult= Label(frameReport,text="Sin Reporte ",font=textoResultado, bg="#CFCFCF").place(relx=0.30, rely=0.17)


#panelReporte = tk.Label(marcoCentral,bg="#CFCFCF").place(relx=0.51, rely=0.18,relheight=0.30, relwidth=0.47)
#EL place la X se mueve para de izquierda a derecha
imgTicket=tk.PhotoImage(file="iconos/boleto32.png")
btnTicket=tk.Button(marcoCentral,image=imgTicket,text=" Ver Tickets ", font=textobotones,compound="left").place(relx=0.51, rely=0.49)

imgNew=tk.PhotoImage(file="iconos/check.png")
btnTicket=tk.Button(marcoCentral,image=imgNew,text=" Nuevo Ticket ", font=textobotones,compound="left").place(relx=0.70, rely=0.49)

imgFactura=tk.PhotoImage(file="iconos/cuenta32.png")
btnFactura=tk.Button(marcoCentral,image=imgFactura,text=" Factura ", font=textobotones,compound="left").place(relx=0.89, rely=0.49)

#-------------------------------------------------Imprimir------------------------------------------------

panelPrint = tk.Label(marcoCentral,bg="#CFCFCF").place(relx=0.51, rely=0.55,relheight=0.30, relwidth=0.47)

imgRefresh=tk.PhotoImage(file="iconos/recargar.png")
btnRefresh=tk.Button(marcoCentral,image=imgRefresh,text=" Nuevo ", font=textobotones,compound="left").place(relx=0.90, rely=0.88)




ventana.mainloop()