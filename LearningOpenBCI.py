#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from yapsy.PluginManager import PluginManager
from scipy import signal
from tkinter import Canvas
from tkinter import Scale
import argparse  # new in Python2.7
import atexit
import logging
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import math, random, threading, time
import numpy as np
import os
import pandas as pd
import serial 
import serial.tools.list_ports
import string
import sys

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font  as tkfont
import threading
import time


LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

def animate(i):
    pullData = open("sampleText.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    a.clear()
    a.plot(xList, yList)
    
def serial_ports():    
    return serial.tools.list_ports.comports()   
def check_cbox1(self, event):
    global bc
    bc = self.combo.get()
    return bc
def check_cbox2(self, event):
    global ar
    ar = self.combo2.get()   
    return ar

class SampleApp(tk.Tk):    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("OpenBCI - Practice")
        container = tk.Frame(self)
        container.pack( fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
class StartPage(tk.Frame):
    def callbackserial(self):
        global com
        com= self.combo.get()
        com=com.replace('- FT231X USB UART','')
        print(com)
    def callbacktime(self):
        global stime
        stime=int (self.slider.get() )   
        print(stime)  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#1959B3")
        self.controller = controller
        
        canvas = Canvas(self,bg="#1959B3",height=583, width=673)
        canvas.pack()
        canvas.create_line(320,157, 320, 500, dash=(6, 4),fill= "white") #Linea punteada
        canvas.place(x=10,y=10) #Linea externa
        
        label = tk.Label(self, text="OpenBCI", font=("Times",70),fg="white", bg="#1959B3")
        label.pack(side="top", fill="x", pady=10)
        label.place(relx=0.32,rely=0.07)
        label2 = tk.Label(self, text="Camila Andrea Navarrete Cataño", fg="white", bg="#1959B3", font=("Verdana")) 
        label2.pack(side="bottom", fill="x", pady=10)
        label2.place(relx=0.08,rely=0.96)
        label3 = tk.Label(self, text="Seleccionar puerto USB:",font=("Helvetica", 17) ,fg="white", bg="#1959B3") 
        label3.pack(fill="x", pady=5)
        label3.place(relx=0.50,rely=0.31)
        label4 = tk.Label(self, text="Bluetooth:",font=("Helvetica", 17) ,fg="white", bg="#1959B3") 
        label4.pack(fill="x", pady=5)
        label4.place(relx=0.50,rely=0.39)
        label6 = tk.Label(self, text="Seleccionar tiempo de grabación:",font=("Helvetica", 17) ,fg="white", bg="#1959B3")
        label6.pack(side="top", fill="x", pady=10)
        label6.place(relx=0.50,rely=0.58)
        label7 = tk.Label(self, text="Este programa le ayudará a interactuar con las interfaces cerebro - computadora mediante el movimiento de una barra virtual y el robot mBot Ranger, en tiempo real."
                          " En la siguiente página podra visualizar la señal de EEG del canal 8, el espectro de frecuencias y la barra  ",
                          font=("Helvetica", 17) ,fg="white", bg="#1959B3", justify="left", wraplength = 250)
        label7.pack(side="top", fill="x", pady=10)
        label7.place(relx=0.1,rely=0.35)
       
        
        button1 = tk.Button(self, text="Iniciar",
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack()
        button1.place(relx=0.64,rely=0.81, height=50, width=80)
        button3 = tk.Button(self, text="OK", command=self.callbackserial)
        button3.pack()
        button3.place(relx=0.87,rely=0.46, height=35, width=60)
        button2 = tk.Button(self, text="OK", command=self.callbacktime)
        button2.pack()
        button2.place(relx=0.87,rely=0.67, height=35, width=60)
        
        number= tk.StringVar()  
        self.combo = ttk.Combobox(self,textvariable=number) #Seleccionar puerto serial
        self.combo.place(x=355, y=285,width=240)
        self.combo["values"] = serial_ports()
        
        self.slider = Scale(self, orient='horizontal',from_=1, to=10, tickinterval=1) #Barra de tiempos
        self.slider.pack()
        self.slider.place(relx=0.50,rely=0.65,width=240)
        
class PageOne(tk.Frame):
    def processing (self):
        global com
        
        logging.basicConfig(level=logging.ERROR)
        manager = PluginManager()   
        get_ipython().run_line_magic('run', 'user.py -p /dev/cu.usbserial-DM00Q8QL --add csv_collect record.csv')
        time.sleep(2.3)
        filelist=os.listdir('./')
        for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
            if not(fichier.endswith(".csv")):
                filelist.remove(fichier)
        filelist.sort(key=lambda x: os.path.getmtime(x))
    
        df2 = pd.read_csv(filelist[-1], delimiter = ',',names=['Tiempo', '1', '2','3','4','5','6','7','8','9'])
        dt = df2.loc[: , "8"]
        data = pd.to_numeric(dt,downcast='signed')
        print (data)
        data[0]=data[2]
        data[1]=data[2]
        fs= 250
        t = np.arange(1,len(data)+1,1)
        t= np.arange(0,(len(data))/fs,(1/fs))
        tsample = 1/fs
        f_low = 40                        
        f_high = 0.5                      
        # Filtro pasa bajas de 50 hz
        b, a = signal.butter(2, 2*f_low/fs, btype='low')
        filt= signal.filtfilt(b, a, data)
        #Filtro pasa altas de 1 hz
        b1, a1 = signal.butter(2, 2*f_high/fs, btype='high') 
        filt1= signal.filtfilt(b1, a1, filt)
        #Filtro Notch
        fstart=(58)/fs*2;
        fstop=(62)/fs*2;
        b2, a2 = signal.butter(2,[fstart,fstop],'bandstop'); # Calculate filter coefficients
        filt2= signal.filtfilt(b2, a2, filt1)
        filt2=filt2/24

        ft = np.abs(np.fft.fft(filt2)) #Magnitud 
        ft = ft[0:int(len(ft)/2)] 
        f = np.linspace(0,fs/2,len(ft))# Vector de frecuencias
    
        #print ("1")
        #plt.figure()
        #ax1 = plt.subplot(2,1,1)
        #plt.plot(t,filt2)
        #plt.title('EEG'),plt.xlabel('Tiempo (s)'),plt.ylabel('Amplitud')
        #plt.grid()
        #ax1 = plt.subplot(2,1,2)
        #plt.plot(f,ft)
        #plt.title('Magnitud de la transformada de Fourier'),plt.xlabel('Frecuencia (Hz)'),plt.ylabel('Amplitud')
        #plt.grid()
        #plt.show()
        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
        a.plot(t,filt2, color='red')
        a.set_ylabel("Amplitud (mV)", fontsize=14)
        a.set_xlabel("Tiempo(s)", fontsize=14)
        canvas3 = FigureCanvasTkAgg(fig, self)
        canvas3.get_tk_widget().pack( expand=True)
        canvas3.get_tk_widget().place(x=20, y=46, height=230, width=500)
        canvas3.draw()
        
        fig1 = Figure(figsize=(6,6))
        b = fig1.add_subplot(111)
        b.plot(f,ft, color='red')
        b.set_ylabel("Amplitud (mV)", fontsize=14)
        b.set_xlabel("Frecuencia (Hz)", fontsize=14)
        canvas4 = FigureCanvasTkAgg(fig1, self)
        canvas4.get_tk_widget().pack( expand=True)
        canvas4.get_tk_widget().place(x=20, y=310, height=230, width=500)
        canvas4.draw()

        
        for i in range(len(f)): 
            f1= f[i]
            if f1 >= 8 and f1<= 14:
                amp=ft[i]
                if amp >=52 and amp <=67:
                    label2 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label2.pack( fill="x", pady=50)
                    label2.place(x=570,y=60,width=100,height=85)
                    label2.update_idletasks()
                    self.update()
                    label3 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label3.pack( fill="x", pady=50)
                    label3.place(x=570,y=165,width=100,height=85)
                    label3.update_idletasks()
                    self.update()
                    label4 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label4.pack( fill="x", pady=50)
                    label4.place(x=570,y=344,width=100,height=85)
                    label4.update_idletasks()
                    self.update()
                    label5 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label5.pack( fill="x", pady=50)
                    label5.place(x=570,y=375,width=100,height=85)
                    label5.update_idletasks()
                    self.update()
                    
                    port="/dev/tty.JDY-31-SPP-Port"
                    bluetooth=serial.Serial(port, 9600)
                    bluetooth.flushInput() 
                    i=0 
                    bluetooth.write(str.encode(str(i)))
                    bluetooth.close()
                    
                    
                elif  amp >67 and amp <=82:
                    label2 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label2.pack( fill="x", pady=50)
                    label2.place(x=570,y=60,width=100,height=85)
                    label2.update_idletasks()
                    self.update()
                    label3 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label3.pack( fill="x", pady=50)
                    label3.place(x=570,y=165,width=100,height=85)
                    label3.update_idletasks()
                    self.update()
                    label4 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label4.pack( fill="x", pady=50)
                    label4.place(x=570,y=270,width=100,height=85)
                    label4.update_idletasks()
                    self.update()
                    label5 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label5.pack( fill="x", pady=50)
                    label5.place(x=570,y=375,width=100,height=85)
                    label5.update_idletasks()
                    self.update()
                    print("Start")
                    port="/dev/tty.JDY-31-SPP-Port"
                    bluetooth=serial.Serial(port, 9600)
                    bluetooth.flushInput() 
                    i=0 
                    bluetooth.write(str.encode(str(i)))
                    bluetooth.close()
                    print("Done")
                elif amp > 82 and amp <=97:
                    label2 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label2.pack( fill="x", pady=50)
                    label2.place(x=570,y=60,width=100,height=85)
                    label2.update_idletasks()
                    self.update()
                    label3 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label3.pack( fill="x", pady=50)
                    label3.place(x=570,y=165,width=100,height=85)
                    label3.update_idletasks()
                    self.update()
                    label4 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label4.pack( fill="x", pady=50)
                    label4.place(x=570,y=270,width=100,height=85)
                    label4.update_idletasks()
                    self.update()
                    label5 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label5.pack( fill="x", pady=50)
                    label5.place(x=570,y=375,width=100,height=85)
                    label5.update_idletasks()
                    self.update()
                    print("Start")
                    port="/dev/tty.JDY-31-SPP-Port"
                    bluetooth=serial.Serial(port, 9600)
                    bluetooth.flushInput() 
                    i=0 
                    bluetooth.write(str.encode(str(i)))
                    bluetooth.close()
                    print("Done")
                elif amp >97 and amp <=112:
                    label2 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label2.pack( fill="x", pady=50)
                    label2.place(x=570,y=60,width=100,height=85)
                    label2.update_idletasks()
                    self.update()
                    label3 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label3.pack( fill="x", pady=50)
                    label3.place(x=570,y=165,width=100,height=85)
                    label3.update_idletasks()
                    self.update()
                    label4 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label4.pack( fill="x", pady=50)
                    label4.place(x=570,y=270,width=100,height=85)
                    label4.update_idletasks()
                    self.update()
                    label5 = tk.Label(text="_____", fg="#b2ebf2", bg="#b2ebf2")
                    label5.pack( fill="x", pady=50)
                    label5.place(x=570,y=375,width=100,height=85)
                    label5.update_idletasks()
                    self.update()
                    print("Start")
                    port="/dev/tty.JDY-31-SPP-Port"
                    bluetooth=serial.Serial(port, 9600)
                    bluetooth.flushInput() 
                    i=0 
                    bluetooth.write(str.encode(str(i)))
                    bluetooth.close()
                    print("Done")
                else: 
                    label2 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label2.pack( fill="x", pady=50)
                    label2.place(x=570,y=60,width=100,height=85)
                    label2.update_idletasks()
                    self.update()
                    label3 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label3.pack( fill="x", pady=50)
                    label3.place(x=570,y=165,width=100,height=85)
                    label3.update_idletasks()
                    self.update()
                    label4 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label4.pack( fill="x", pady=50)
                    label4.place(x=570,y=270,width=100,height=85)
                    label4.update_idletasks()
                    self.update()
                    label5 = tk.Label(text="_____", fg="#1959B3", bg="#1959B3")
                    label5.pack( fill="x", pady=50)
                    label5.place(x=570,y=375,width=100,height=85)   
                    label5.update_idletasks()
                    self.update()
                    
    def callback1(self):
        global t0
        global t1
        global po
        global stime
        t0 = time.process_time
        if stime == 1: 
            t0 = time.time()
            t1=0
            while t1<= 60:
                self.processing()
                self.update()
                t1= time.time()-t0
            
        elif stime == 2:
            t0 = time.time()
            t1=0
            while t1<= 120:
                self.processing()
                t1= time.time()-t0
                print (t1)
        elif stime == 3: 
            t0 = time.time()
            t1=0
            while t1<= 180:
                self.processing()
                t1= time.time()-t0
                print (t1)
        elif stime == 4:
            t0 = time.time()
            t1=0
            while t1<= 240:
                self.processing()
                t1= time.time()-t0
                print (t1)
        elif stime == 5: 
            t0 = time.time()
            t1=0
            while t1<= 300:
                self.processing()
                t1= time.time()-t0
                print (t1)
        elif stime == 6:
            t0 = time.time()
            t1=0
            while t1<= 360:
                self.processing()
                t1= time.time()-t0
                print (t1)
        elif stime == 7: 
            t0 = time.time()
            t1=0
            while t1<= 420:
                self.processing()
                t1= time.time()-t0
                print (t1)
        elif stime == 8:
            t0 = time.time()
            t1=0
            while t1<= 480:
                self.processing()
                t1= time.time()-t0
                print (t1)
        elif stime == 9: 
            t0 = time.time()
            t1=0
            while t1<= 540:
                self.processing()
                t1= time.time()-t0
                print (t1)   
        elif stime == 10: 
            t0 = time.time()
            t1=0
            while t1<= 600:
                self.processing()
                t1= time.time()-t0
                print (t1)    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#1959B3")
        self.controller = controller

        canvas1 = Canvas(self,bg="#1959B3",height=537, width=530)
        canvas1.pack()
        canvas1.place(x=5,y=5)
        canvas2 = Canvas(self,bg="#1959B3",height=537, width=135)
        canvas2.pack()
        canvas2.place(x=550,y=5)
        button = tk.Button(self, text="Volver",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom", pady=10)
        button.place(x=30, y=560, height=30, width=90)
        button2 = tk.Button(self, text="Iniciar",command=self.callback1)
        button2.pack(side="bottom", pady=10)
        button2.place(x=200, y=560, height=30, width=180)
        canvas3 = FigureCanvasTkAgg(f, self)
        canvas3.draw()
        canvas3.get_tk_widget().pack( expand=True)
        canvas3.get_tk_widget().place(x=20, y=46, height=230, width=500)
        canvas4 = FigureCanvasTkAgg(f, self)
        canvas4.draw()
        canvas4.get_tk_widget().pack(side=tk.LEFT, expand=True)
        canvas4.get_tk_widget().place(x=20, y=310, height=230, width=500) 
        label = tk.Label(self, text="SEÑAL DE EEG EN EL TIEMPO (CANAL 8)", font=("Times",15),fg="white", bg="#1959B3")
        label.pack(side="top", fill="x", pady=10)
        label.place(x=140,y=20)
        label1 = tk.Label(self, text="TRANSFORMADA DE FOURIER", font=("Times",15),fg="white", bg="#1959B3")
        label1.pack(side="top", fill="x", pady=10)
        label1.place(x=170,y=283)
        label2 = tk.Label(self,text="_____", fg="#1959B3", bg="#1959B3")
        label2.pack( fill="x", pady=50)
        label2.place(x=570,y=60,width=100,height=85)
        label3 = tk.Label(self,text="_____", fg="#1959B3", bg="#1959B3")
        label3.pack( fill="x", pady=50)
        label3.place(x=570,y=165,width=100,height=85)
        label4 = tk.Label(self,text="_____", fg="#1959B3", bg="#1959B3")
        label4.pack( fill="x", pady=50)
        label4.place(x=570,y=270,width=100,height=85)
        label5 = tk.Label(self,text="_____", fg="#1959B3", bg="#1959B3")
        label5.pack( fill="x", pady=50)
        label5.place(x=570,y=375,width=100,height=85)
    
if __name__ == "__main__":
    app = SampleApp()
    com = "COM1"
    stime = 1
    app.geometry("700x610+440+20")
    ani = animation.FuncAnimation(f, animate, interval=1000)
    app.mainloop()       


# In[ ]:




