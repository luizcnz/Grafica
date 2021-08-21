# Examen.py
from tkinter import *
import tkinter as tk
import os
from tkinter.constants import RIGHT, TOP, X
import tkinter.font as TkFont
from tkinter import Frame, Label, ttk
import time
import tkinter.messagebox as MessageBox
import tkinter.scrolledtext as ScrolledText
import array 

import subprocess
import time

import cv2
from cv2 import data
from pymysql.connections import Connection
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
import pymysql
from datetime import date

ventana = tk.Tk()
ventana.geometry("1250x750")
ventana.title("Peajes")
ventana.resizable(0,0)

num = 1
image = cv2.imread('Fotos/auto1.jpg')
ubicacionPeaje=2
today = date.today()
textoplaca = 'HBE 9052'

# Area de funciones
def rotar():
    global textoplaca
    global num
    vehiculosFotos = ["auto1.png","auto2.png"]
    auto = PhotoImage(file="Fotos/"+vehiculosFotos[num])
    global image 

    vehiculosPlacas = ["auto1.jpg","auto2.jpg"]
    image = cv2.imread('Fotos/'+vehiculosPlacas[num])

    panel.configure(image=auto)
    panel.image = auto
    if num >= 1:
        num=0
    else:
        num+=1

def ticket():

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(3,3))
    canny = cv2.Canny(gray,150,200)
    cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    vuelta = 0
    for c in cnts:
        #contar=contar+1
        area = cv2.contourArea(c)

        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.05*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        
        if len(approx)==4 and area>9000:
            print('area=',area)
            vuelta=vuelta+1
            
            aspect_ratio = float(w)/h
            
            if aspect_ratio>2:
                placa = gray[y:y+h,x:x+w]
                txt = pytesseract.image_to_string(placa,config='--psm 12')
                split_string = txt.split()
                textoplaca = split_string[0]+" "+split_string[1]
                #text = pytesseract.image_to_string(image)


    class DataBase:
        def __init__(self):#coneccion con la base de datos
            self.connection=pymysql.connect(host='173.249.21.6', user='movil2',password='carwash2021',db='ProyectoFinal_Python')

            self.cursor = self.connection.cursor()
            print("Conexion Exitosa!!!")

        def seleccionar(self):#inseercion de datos
            div = textoplaca.split()
            dbplaca = div[0]+" "+div[1]
            sql='SELECT * FROM Vehiculos where Placa = "'+str(dbplaca)+'"'

            print("query: ",sql)
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                rows = self.cursor.fetchall()
                for row in rows:
                    print(row)
                
                idVehicle = row[0]
                idVehicleType = row[4]
                print("prueba con el id del tipo de auto:",idVehicleType)
            
            except Exception as e:
                raise

            sql2='SELECT IdTarifaPeaje,precio FROM TarifaPeaje where IdTipoVehiculo = "'+str(idVehicleType)+'" and IdPeaje = "'+str(ubicacionPeaje)+'"'

            print("query: ",sql2)
            try:
                self.cursor.execute(sql2)
                self.connection.commit()
                rows2 = self.cursor.fetchall()
                for row2 in rows2:
                    print(row2[0])
                
                idTariff = row2[0]
                price = row2[1]
                print("Precio del auto:",price)
            
            except Exception as e:
                raise

            sql3='INSERT into Ticket(Fecha, IdVehiculos, IdTarifaPeaje, Subtotal) VALUES ("'+str(today)+'", '+str(idVehicle)+', '+str(idTariff)+', '+str(price)+')'
            print("query: ",sql3)
            
            try:
                self.cursor.execute(sql3)
                self.connection.commit()
                print("Se Guardo Con Exito La Consulta: ",sql3)#confirmacion de guardado
                
            except Exception as e:
                    raise

        
    
    print('PLACA: ',textoplaca)
            
    database = DataBase()
    #database.ingresar()
    database.seleccionar()



def factura():

    placaFactura = textoplaca
    detailsPrices = array.array('i', [])
    details = array.array('i', [])
    class DataBase:
        def __init__(self):#coneccion con la base de datos
            self.connection=pymysql.connect(host='173.249.21.6', user='movil2',password='carwash2021',db='ProyectoFinal_Python')

            self.cursor = self.connection.cursor()
            print("Conexion Exitosa!!!")

        def genFactura(self):#inseercion de datos

            sql='SELECT * FROM Vehiculos where Placa = "'+str(placaFactura)+'"'

            print("query: ",sql)
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                rows = self.cursor.fetchall()
                for row in rows:
                    print(row)
                
                idVehicle = row[0]
                print("prueba con el id del auto:",idVehicle)
            
            except Exception as e:
                raise

            sql2='SELECT * FROM Ticket where IdVehiculos = "'+str(idVehicle)+'"'
            print("query2: ",sql2)
            

            try:
                price=0
                self.cursor.execute(sql2)
                self.connection.commit()
                rows = self.cursor.fetchall()
                for row in rows:
                    print(row)
                    price = price+row[4]
                    details.append( row[0])
                    detailsPrices.append( row[4])
                
                idTariff = row[0]
                
                print("Total de la Factura:",price)
                print("Array de tickets: ",details)
            except Exception as e:
                raise

            sql3='INSERT into Factura(IdVehiculos, Total, Fecha, IdEstadoFactura) VALUES ('+str(idVehicle)+', '+str(price)+', "'+str(today)+'", 1)'
            print("query3: ",sql3)

            try:
                price=0
                self.cursor.execute(sql3)
                self.connection.commit()
                rows = self.cursor.fetchall()
                idFactura = self.cursor.lastrowid
                i=0

                for detalle in details:
                    
                    sql4='INSERT into DetalleFactura(IdFactura, IdTicket, Precio) VALUES ('+str(idFactura)+','+str(detalle)+', '+str(detailsPrices[i])+')'
                    print("query4: ",sql4)
                    self.cursor.execute(sql4)
                    self.connection.commit()
                    print("Se Guardo Con Exito La Consulta: ",sql4)#confirmacion de guardado

                i=i+1

            
            except Exception as e:
                raise
            
            
    database = DataBase()
    database.genFactura()



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
panel = tk.Label(marcoCentral, image = auto, width=600,height=500)
panel.place(relx=0.02, rely=0.18)


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
btnTicket=tk.Button(marcoCentral,image=imgNew,text=" Nuevo Ticket ", command=ticket,font=textobotones,compound="left").place(relx=0.70, rely=0.49)

imgFactura=tk.PhotoImage(file="iconos/cuenta32.png")
btnFactura=tk.Button(marcoCentral,image=imgFactura,text=" Factura ", command=factura, font=textobotones,compound="left").place(relx=0.89, rely=0.49)

#-------------------------------------------------Imprimir------------------------------------------------

panelPrint = tk.Label(marcoCentral,bg="#CFCFCF").place(relx=0.51, rely=0.55,relheight=0.30, relwidth=0.47)

imgRefresh=tk.PhotoImage(file="iconos/recargar.png")
btnRefresh=tk.Button(marcoCentral,image=imgRefresh,text=" Nuevo ", command=rotar, font=textobotones,compound="left").place(relx=0.90, rely=0.88)




ventana.mainloop()