# Examen.py

import tkinter as tk
import os
import tkinter.font as TkFont
import time
import tkinter.messagebox as MessageBox
import tkinter.scrolledtext as ScrolledText

import cv2
from cv2 import data
from pymysql.connections import Connection
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
import pymysql
import array
from datetime import date

import subprocess
import time

v0 = tk.Tk()
v0.geometry("850x500+0+0")
v0.title("Examen")

today = date.today()
ubicacionPeaje=2

image = cv2.imread('Fotos/HBI7145.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#cada una de estas propiedades son variaciones de la imagen que nos pueden servir para poder detectar la placa
gray = cv2.blur(gray,(3,3))
canny = cv2.Canny(gray,150,200)
#coloca los colores blancos mas resaltados
#canny = cv2.dilate(canny,None,iterations=1)

#Encontrar los contronos de la imagen atraves de las propiedades que anteriormente
#_,cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

#Dibuja todos los contornos encontrados
#cv2.drawContours(image,cnts,-1,(0,255,0),2)

#Reccorer los contornos

# Configuracion de texto
text1=TkFont.Font(family="Arial",size=12)



# Zona de Imagenes


# Zona de funciones

def ticket():
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
                txt = pytesseract.image_to_string(placa,config='--psm 10')
                split_string = txt.split()
                texto = split_string[0]+" "+split_string[1]
                #text = pytesseract.image_to_string(image)

                #cv2.imshow('PLACA',placa)
                #cv2.moveWindow('PLACA',780,10)
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
                cv2.putText(image,texto,(x-20,y-10),1,2.2,(0,255,0),3)

    # class DataBase:
    #     def __init__(self):#coneccion con la base de datos
    #         self.connection=pymysql.connect(host='173.249.21.6', user='movil2',password='carwash2021',db='ProyectoFinal_Python')

    #         self.cursor = self.connection.cursor()
    #         print("Conexion Exitosa!!!")

    #     def seleccionar(self):#inseercion de datos
    #         div = texto.split()
    #         dbplaca = div[0]+" "+div[1]
    #         sql='SELECT * FROM Vehiculos where Placa = "'+str(dbplaca)+'"'

    #         print("query: ",sql)
    #         try:
    #             #self.cursor.execute(sql)
    #             #self.connection.commit()
    #             rows = self.cursor.fetchall()
    #             for row in rows:
    #                 print(row)
                
    #             idVehicle = row[0]
    #             idVehicleType = row[4]
    #             print("prueba con el id del tipo de auto:",idVehicleType)
            
    #         except Exception as e:
    #             raise

    #         sql2='SELECT IdTarifaPeaje,precio FROM TarifaPeaje where IdTipoVehiculo = "'+str(idVehicleType)+'" and IdPeaje = "'+str(ubicacionPeaje)+'"'

    #         print("query: ",sql2)
    #         try:
    #             #self.cursor.execute(sql2)
    #             #self.connection.commit()
    #             rows2 = self.cursor.fetchall()
    #             for row2 in rows2:
    #                 print(row2[0])
                
    #             idTariff = row2[0]
    #             price = row2[1]
    #             print("Precio del auto:",price)
            
    #         except Exception as e:
    #             raise

    #         sql3='INSERT into Ticket(Fecha, IdVehiculos, IdTarifaPeaje, Subtotal) VALUES ("'+str(today)+'", '+str(idVehicle)+', '+str(idTariff)+', '+str(price)+')'
    #         print("query: ",sql3)
            
    #         try:
    #             self.cursor.execute(sql3)
    #             self.connection.commit()
    #             print("Se Guardo Con Exito La Consulta: ",sql3)#confirmacion de guardado
                
    #         except Exception as e:
    #                 raise

        
    
    print('PLACA: ',texto)
    cv2.imshow('Image',image)
    cv2.moveWindow('Image',45,10)
            
    # database = DataBase()
    # #database.ingresar()
    # database.seleccionar()


    #label_variable=tk.Label(v0,text=""+str(DataBase.sql)+"",font=escanear.datos).place(x=450,y=50)


def factura():

    placaFactura="HBE 9052"
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
                #self.cursor.execute(sql)
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
                #self.cursor.execute(sql2)
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
                #self.cursor.execute(sql3)
                self.connection.commit()
                rows = self.cursor.fetchall()
                idFactura = self.cursor.lastrowid
                i=0

                for detalle in details:
                    
                    sql4='INSERT into DetalleFactura(IdFactura, IdTicket, Precio) VALUES ('+str(idFactura)+','+str(detalle)+', '+str(detailsPrices[i])+')'
                    print("query4: ",sql4)
                    #self.cursor.execute(sql4)
                    self.connection.commit()
                    print("Se Guardo Con Exito La Consulta: ",sql4)#confirmacion de guardado

                i=i+1

            
            except Exception as e:
                raise
            
            
    database = DataBase()
    database.genFactura()
            


# Etiquetas
#-----------------------------
label_fijo=tk.Label(v0,text="Prueba de Texto:",font=text1).place(x=300,y=50)
# label_minini=tk.Label(v0,text="Minuto Inicial:",font=text1).place(x=300,y=80)
# label_horaf=tk.Label(v0,text="Hora Final:",font=text1).place(x=300,y=110)
# label_minif=tk.Label(v0,text="Hora Inicial:",font=text1).place(x=300,y=140)




# Variables
global horai
global minini
global horaf
global minif

minini=tk.StringVar()
horaf=tk.StringVar()
minif=tk.StringVar()

# Cajas de texto
#-----------------------------

# txt_minini=tk.Entry(v0,textvariable=minini,width=5).place(x=400,y=80)
# txt_horaf=tk.Entry(v0,textvariable=horaf,width=5).place(x=400,y=110)
# txt_minif=tk.Entry(v0,textvariable=minif,width=5).place(x=400,y=140)

# Botones
#-----------------------------
btn_save=tk.Button(v0,text="Escanear",command=ticket).place(x=400,y=180)
btn_save=tk.Button(v0,text="factura",command=factura).place(x=400,y=123)
# btn_on=Button(v0,text="ON",command=on_local).place(x=400, y=220)
# btn_off=Button(v0,text="OFF",command=off_local).place(x=400, y=260)
# btn_exit=Button(v0,text="Salir",command=exit).place(x=400, y=400)



v0.mainloop()