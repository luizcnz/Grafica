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
import numpy as np

import subprocess
import time

import cv2
from cv2 import data, imshow
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
ubicacionPeaje=1
today = date.today()
textoplaca = 'HBE 9052'


# Area de funciones

def buscar():

    if cmbUbication.get()=="Marcovia":
        ubicacionPeaje=1
    if cmbUbication.get()=="Choluteca":
        ubicacionPeaje=2
    if cmbUbication.get()=="San Lorenzo":
        ubicacionPeaje=3

    print("Lugar de peaje: ",cmbUbication.get())
    print("ID del Lugar de peaje: ",ubicacionPeaje)
    lblUbicationResult.configure(text=cmbUbication.get())

    #deteccion de la placa del auto cuando se rotan o buscan----------------------------
    
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
                txt = pytesseract.image_to_string(placa,config='--psm 10')
                split_string = txt.split()
                textoplaca = split_string[0]+" "+split_string[1]
    
                lblPlacaText.configure(text=textoplaca)
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
                cv2.putText(image,textoplaca,(x-20,y-10),1,2.2,(0,255,0),3)
                # panel.configure(image=image)
                # panel.image = image
                #imshow("imagen",image)

    #fin de la deteccion de la placa del auto ------------------------

    class DataBase:
        def __init__(self):#coneccion con la base de datos
            self.connection=pymysql.connect(host='173.249.21.6', user='movil2',password='carwash2021',db='ProyectoFinal_Python')

            self.cursor = self.connection.cursor()
            print("Conexion Exitosa!!!")

        def seleccionar(self):#inseercion de datos
            div = textoplaca.split()
            dbplaca = div[0]+" "+div[1]
            sql='SELECT Entidad.Nombre, Entidad.Ubicacion, Vehiculos.IDVehiculos FROM Entidad INNER JOIN Vehiculos ON Vehiculos.IdEntidad = Entidad.IdEntidad  where Placa = "'+str(dbplaca)+'"'

            print("query: ",sql)
            try:
                self.cursor.execute(sql)
                self.connection.commit()
                rows = self.cursor.fetchall()
                for row in rows:
                    print(row)
                
                entidadnombre = row[0]
                entidadlugar = row[1]
                vehiculoid=row[2]
                print("Datos obtenidos, Nombre: ",entidadnombre, "Lugar: ", entidadlugar)

                lblOwnerResult.configure(text=entidadnombre)
                lblUbicationResult.configure(text=entidadlugar)
            
            except Exception as e:
                raise

            sql2='SELECT Reporte.Detalle, TipoReporte.DetalleReporte from Reporte INNER JOIN TipoReporte ON Reporte.IdTipoReporte = TipoReporte.IdTipoReporte WHERE Reporte.idVehiculos =  "'+str(vehiculoid)+'"'
            print("query2: ",sql2)
            
            report=[]
            detailreport=[]

            try:
                self.cursor.execute(sql2)
                self.connection.commit()
                rows = self.cursor.fetchall()
                indexlist=1
                for row in rows:
                    print(row)
                    report.append( row[0])
                    detailreport.append( row[1])
                    listdata = "Reporte: "+row[0]+" - Tipo de Reporte: "+row[1]
                    lblReportResult.insert(indexlist,listdata)
                
                print("Reportes:",report)
                print("Detalles: ",detailreport)

                
                indexlist=+1
            except Exception as e:
                raise

    print('PLACA: ',textoplaca)
            
    database = DataBase()
    database.seleccionar()


#Funcion para cambiar la imagen del vehiculo con una nueva
def rotar():
    global ubicacionPeaje
    global textoplaca
    global num

    if cmbUbication.get()=="Marcovia":
        ubicacionPeaje=1
    if cmbUbication.get()=="Choluteca":
        ubicacionPeaje=2
    if cmbUbication.get()=="San Lorenzo":
        ubicacionPeaje=3

    print("Lugar de peaje: ",cmbUbication.get())
    print("ID del Lugar de peaje: ",ubicacionPeaje)
    lblUbicationResult.configure(text=cmbUbication.get())

    
    vehiculosFotos = ["auto1.png","auto2.png","auto3.png","auto4.png","auto5.png","auto6.png","auto7.png","auto8.png","auto9.png","auto10.png"]
    auto = PhotoImage(file="Fotos/"+vehiculosFotos[num])

    global image 
    vehiculosPlacas = ["auto1.jpg","auto2.jpg","auto3.jpg","auto4.jpg","auto5.jpg","auto6.jpg","auto7.jpg","auto8.jpg","auto9.jpg","auto10.jpg"]
    image = cv2.imread('Fotos/'+vehiculosPlacas[num])

    panel.configure(image=auto)
    panel.image = auto
    #print(num)
    if num == 9:
        num=0
    else:
        num+=1

#Funcion para generar un ticket que se guardarae en la base de datos
def ticket():
    graytemplate = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
                txt = pytesseract.image_to_string(placa,config='--psm 10')
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


    #inicio del Match Template

    def points_template_matching(image, template):
        points = []
        threshold = 0.9
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        candidates = np.where(res >= threshold)
        candidates = np.column_stack([candidates[1], candidates[0]])
        i = 0
        while len(candidates) > 0:
            if i == 0: points.append(candidates[0])
            else:
                to_delete = []
                for j in range(0, len(candidates)):
                    diff = points[i-1] - candidates[j]
                    if abs(diff[0]) < 10 and abs(diff[1]) < 10:
                        to_delete.append(j)
                candidates = np.delete(candidates, to_delete, axis=0)
                if len(candidates) == 0: break
                points.append(candidates[0])
            i += 1
        return points

    # imshow("plantilla",graytemplate)

    marca1 = cv2.imread("Fotos/ford1.jpg", 0)
    marca2 = cv2.imread("Fotos/ford2.jpg", 0)
    marca3 = cv2.imread("Fotos/honda1.jpg", 0)
    marca4 = cv2.imread("Fotos/hyundai1.jpg", 0)
    marca5 = cv2.imread("Fotos/hyundai2.jpg", 0)
    marca6 = cv2.imread("Fotos/hyundai3.jpg", 0)
    marca7 = cv2.imread("Fotos/nissan1.jpg", 0)
    marca8 = cv2.imread("Fotos/toyota1.jpg", 0)
    marca9 = cv2.imread("Fotos/toyota2.jpg", 0)
    marca10 = cv2.imread("Fotos/toyota3.jpg", 0)

    # imshow("plantilla1",marca1)
    # imshow("plantilla2",marca2)
    # imshow("plantilla3",marca3)
    # imshow("plantilla4",marca4)
    # imshow("plantilla5",marca5)
    # imshow("plantilla6",marca6)
    # imshow("plantilla7",marca7)
    # imshow("plantilla8",marca8)
    # imshow("plantilla9",marca9)
    # imshow("plantilla10",marca10)

    logo1 = points_template_matching(graytemplate, marca1)
    logo2 = points_template_matching(graytemplate, marca2)
    logo3 = points_template_matching(graytemplate, marca3)
    logo4 = points_template_matching(graytemplate, marca4)
    logo5 = points_template_matching(graytemplate, marca5)
    logo6 = points_template_matching(graytemplate, marca6)
    logo7 = points_template_matching(graytemplate, marca7)
    logo8 = points_template_matching(graytemplate, marca8)
    logo9 = points_template_matching(graytemplate, marca9)
    logo10 = points_template_matching(graytemplate, marca10)

    ford=False
    honda=False
    hyundai=False
    nissan=False
    toyota=False

    if((len(logo1)>0)or(len(logo2)>0)):
        ford=True

    if((len(logo3)>0)):
        honda=True

    if((len(logo4)>0)or(len(logo5)>0)or(len(logo6)>0)):
        hyundai=True

    if((len(logo7)>0)):
        nissan=True
    
    if((len(logo8)>0)or(len(logo9)>0)or(len(logo10)>0)):
        toyota=True

    if ford==True:
        marcaVehiculo="ford"
        print(marcaVehiculo)
    if honda==True:
        marcaVehiculo="honda"
        print(marcaVehiculo)
    if hyundai==True:
        marcaVehiculo="hyundai"
        print(marcaVehiculo)
    if nissan==True:
        marcaVehiculo="nissan"
        print(marcaVehiculo)
    if toyota==True:
        marcaVehiculo="toyota"
        print(marcaVehiculo)

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


#funcion para generar una factura en base a los tickets del vehiculo
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
cmbUbication=ttk.Combobox(marcoCentral,width=30, values=["Marcovia","Choluteca","San Lorenzo"], state='readonly')
cmbUbication.place(relx=0.15, rely=0.12)

cmbUbication.set("Marcovia")

#------------------------------------IMAGEN DEL CARRO----------------------------------
auto = tk.PhotoImage(file="Fotos/auto1.png")
panel = tk.Label(marcoCentral, image = auto, width=600,height=500)
panel.place(relx=0.02, rely=0.18)


#------------------------------------LABEL FINAL----------------------------------
lblPlaca=tk.Label(marcoCentral,text="Numero de Placa Detectado: ",font=textoEtiqueta,bg="#E3E1E1").place(relx=0.02, rely=0.88)
lblPlacaText=tk.Label(marcoCentral,text=textoplaca,font=textoEtiqueta,bg="#E3E1E1")
lblPlacaText.place(relx=0.22, rely=0.88)

#txtPlaca=tk.Entry(marcoCentral,width=30,justify=tk.RIGHT).place(relx=0.22, rely=0.89)

imgSearch=tk.PhotoImage(file="iconos/buscar32.png")
btnSearch=tk.Button(marcoCentral,image=imgSearch,text=" Buscar ", command=buscar, font=textobotones,compound="left").place(relx=0.38, rely=0.88)

#------------------------------------REPORTE -------------------------------------------------------
frameReport = Frame()
frameReport.place(relx=0.51, rely=0.18,relheight=0.30, relwidth=0.47)
frameReport.config(bg="#CFCFCF")
lblOwner= Label(frameReport,text="Titular del Vehiculo: ",font=textoEnunciado, bg="#CFCFCF").place(relx=0.01, rely=0.03)
lblOwnerResult= Label(frameReport,text="Prueba ",font=textoResultado, bg="#CFCFCF")
lblOwnerResult.place(relx=0.30, rely=0.03)

lblUbication= Label(frameReport,text="Ubicacion: ",font=textoEnunciado, bg="#CFCFCF").place(relx=0.70, rely=0.03)
lblUbicationResult= Label(frameReport,text="SPS",font=textoResultado, bg="#CFCFCF")
lblUbicationResult.place(relx=0.85, rely=0.03)

lblReport= Label(frameReport,text="Reporte: ",font=textoEnunciado, bg="#CFCFCF").place(relx=0.01, rely=0.17)
lblReportResult= Listbox(frameReport,font=textoResultado, bg="#CFCFCF", width=60, height=8)
lblReportResult.place(relx=0.15, rely=0.17)


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