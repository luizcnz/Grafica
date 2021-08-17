# Examen.py

import tkinter as tk
import os
import tkinter.font as TkFont
import time
import tkinter.messagebox as MessageBox
import tkinter.scrolledtext as ScrolledText

import subprocess
import time

v0 = tk.Tk()
v0.geometry("550x500+0+0")
v0.title("Examen")

# Zona de Imagenes
# img_on=tk.PhotoImage(file="on.png")
# img_off=tk.PhotoImage(file="off.png")

# # Zona de funciones

# def on_local():
#                os.system("sudo /./home/carlos/on.sh")
#                os.system("sudo /etc/ssmtp/send_on.sh &")
# def off_local():
#                 os.system("sudo /./home/carlos/off.sh")
#                 os.system("sudo /etc/ssmtp/send_off.sh &")

# def update():
    
#              pf17=open("/home/carlos/gpio17.txt","r")
#              for linea in pf17:
#                              field=linea.split("\n")
#                              fieldf=field[0]
#                              if(fieldf=="0"):
#                                             btn_on=tk.Button(v0,image=img_off).place(x=100,y=50)
                                            
                                            
#                              if(fieldf=="1"):
#                                             btn_on=tk.Button(v0,image=img_on).place(x=100,y=50)
                                            
#              pf21=open("/home/carlos/gpio21.txt","r")
#              for linea in pf21:
#                              field=linea.split("\n")
#                              fieldf=field[0]
#                              if(fieldf=="1"):
#                                             btn_on=tk.Button(v0,image=img_on).place(x=100,y=160)
                                            
#                              if(fieldf=="0"):
#                                             btn_on=tk.Button(v0,image=img_off).place(x=100,y=160)
                                            
                                            
#              pf27=open("/home/carlos/gpio27.txt","r")
#              for linea in pf27:
#                              field=linea.split("\n")
#                              fieldf=field[0]
#                              if(fieldf=="0"):
#                                             btn_on=tk.Button(v0,image=img_off).place(x=100,y=270)
#                                             v0.after(1000,update)
#                              if(fieldf=="1"):
#                                             btn_on=tk.Button(v0,image=img_on).place(x=100,y=270)
#                                             v0.after(1000,update)
                                            

# update()




# def clean():
#             horai.set('')
#             minini.set('')
#             horaf.set('')
#             minif.set('')

# def save():
#             # Variables capturadas por el usuario
#             hi=horai.get()
#             mi=minini.get()
#             hf=horaf.get()
#             mf=minif.get()

#             # Variables de tipo constante
#             dia="*"
#             mes="*"
#             ano="*"
#             tab=" "
#             user="root"
#             path1="/home/carlos/on.sh"
#             path2="/home/carlos/off.sh"
#             mail1="/etc/ssmtp/send_on.sh &"
#             mail2="/etc/ssmtp/send_off.sh &"

#             # Dar full acceso a nivel de permiso de lectura, escritura y ejecucion
#             # chmod -R 777
#             os.system("sudo chmod -R 777 /etc/cron.d/accion1")
#             os.system("sudo chmod -R 777 /etc/cron.d/accion2")
#             os.system("sudo chmod -R 777 /etc/cron.d/accion3")
#             os.system("sudo chmod -R 777 /etc/cron.d/accion4")

#             cadena1=(str(mi)+''+str(tab)+''+str(hi)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(ano)+''+str(tab)+''+str(user)+''+str(tab)+''+str(path1))
#             correo1=(str(mi)+''+str(tab)+''+str(hi)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(ano)+''+str(tab)+''+str(user)+''+str(tab)+''+str(mail1))
#             cadena2=(str(mf)+''+str(tab)+''+str(hf)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(ano)+''+str(tab)+''+str(user)+''+str(tab)+''+str(path2))
#             correo2=(str(mf)+''+str(tab)+''+str(hf)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(ano)+''+str(tab)+''+str(user)+''+str(tab)+''+str(mail2))

#             # Abrir apuntador de archivo para CADENA1
#             pf1=open(r'/etc/cron.d/accion1','w')
#             pf1.write(cadena1)
#             pf1.write("\n")
#             pf1.close()
#             # Abrir apuntador de archivo para CADENA2
#             pf2=open(r'/etc/cron.d/accion2','w')
#             pf2.write(cadena2)
#             pf2.write("\n")
#             pf2.close()

#             # Abrir apuntador de archivo para mail1
#             pf3=open(r'/etc/cron.d/accion3','w')
#             pf3.write(correo1)
#             pf3.write("\n")
#             pf3.close()
#             # Abrir apuntador de archivo para mail2
#             pf4=open(r'/etc/cron.d/accion4','w')
#             pf4.write(correo2)
#             pf4.write("\n")
#             pf4.close()
#             time.sleep(0.1)
            
#             # Revertir permisos
#             os.system("sudo chmod -R 755 /etc/cron.d/accion1")
#             os.system("sudo chmod -R 755 /etc/cron.d/accion2")
#             os.system("sudo chmod -R 755 /etc/cron.d/accion3")
#             os.system("sudo chmod -R 755 /etc/cron.d/accion4")

#             # REinicio con el servicio cron
#             os.system("sudo /etc/init.d/cron restart")

#             clean()
#             MessageBox.showinfo(message="Proceso Realizado")


def tiempo():
             text1=TkFont.Font(family="Arial", size=20)
             t=time.strftime("%H:%M:%S")
             label_tiempo=tk.Label(v0,text=t,font=text1).place(x=250, y=400)
             v0.after(1000,tiempo)

tiempo()

            
# Configuracion de texto
text1=TkFont.Font(family="Arial",size=12)

# Etiquetas
label_horai=tk.Label(v0,text="Hora Inicial:",font=text1).place(x=300,y=50)
label_minini=tk.Label(v0,text="Minuto Inicial:",font=text1).place(x=300,y=80)
label_horaf=tk.Label(v0,text="Hora Final:",font=text1).place(x=300,y=110)
label_minif=tk.Label(v0,text="Hora Inicial:",font=text1).place(x=300,y=140)




# Variables
global horai
global minini
global horaf
global minif
horai=tk.StringVar()
minini=tk.StringVar()
horaf=tk.StringVar()
minif=tk.StringVar()

# Cajas de texto
txt_horai=tk.Entry(v0,textvariable=horai,width=5).place(x=400,y=50)
# txt_minini=Entry(v0,textvariable=minini,width=5).place(x=400,y=80)
# txt_horaf=Entry(v0,textvariable=horaf,width=5).place(x=400,y=110)
# txt_minif=Entry(v0,textvariable=minif,width=5).place(x=400,y=140)

# Botones
btn_save=tk.Button(v0,text="save",command=tiempo).place(x=400,y=180)
# btn_on=Button(v0,text="ON",command=on_local).place(x=400, y=220)
# btn_off=Button(v0,text="OFF",command=off_local).place(x=400, y=260)
# btn_exit=Button(v0,text="Salir",command=exit).place(x=400, y=400)

v0.mainloop()