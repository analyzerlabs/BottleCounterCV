from InterfazLcd import *
from imageProcessing import *
import RPi.GPIO as GPIO
import time
import numpy as np

class maquina:
    Interfaz = InterfazLCD(1)
    imp = ImgProcessing(0)
    encoder_data     = 27
    encoder_clock   = 22
    encoder_buttom  = 17
    cadena = []

    def __init__(self):
        self.state = 0
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)
        GPIO.setup(self.encoder_clock, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.encoder_data, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.encoder_buttom, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self.encoder_clock, GPIO.BOTH, callback=self.encoder_interrupt,bouncetime=100)  # add both edge detection on a channel
        GPIO.add_event_detect(self.encoder_buttom, GPIO.RISING, callback=self.buttom_interrupt,bouncetime=100)  # add both edge detection on a channel
    
    def __del__(self):
        GPIO.cleanup()
    
    def encoder_interrupt(self,channel):
        self.cadena = str(GPIO.input(self.encoder_clock))+str(GPIO.input(self.encoder_data))
    
    def buttom_interrupt(self,channel):
        self.cadena = 'p'

    def print_menu(self,argument):
        switcher = { 
            0: "Bottle Counter Menu", 
            1: "Start Counting", 
            2: "Calibrate Counting",
            3: "Reset Counting", 
        }
        print(switcher.get(argument, "Nothing"))
        Interfaz.show_menu()

    def finish_function(self):
        while(1):
            if self.cadena == 'p':
                break
        self.cadena = 'np'  #no pressed
        self.state = 0
    
    def function_1(self):
        found = False
        ctr = 0
        data = np.loadtxt(fname = "/home/pi/BottleCounterCV/threshold.dat")
        print ("Calibration Data: "+str(data))
        maxT=data[0]
        minT=data[1]
        while(self.imp.cap.isOpened()):
            t1,t2 = self.imp.getValue()
            minT,maxT = self.Interfaz.get_threshold()
            if t1 > maxT or t2 < minT:
                found = True
                ctr = 0
            else:
                ctr = ctr + 1
            if ctr == 8:
                if found:
                    self.Interfaz.addCounter()
                    self.Interfaz.save_data()
                found = False
                ctr = 0
            print(self.Interfaz.counter)
            if self.cadena == 'p':
                break
        self.state = 0

    def function_2(self):
        gvalues1 = []
        gvalues2 = []
        t0 = int(round(time.time() * 1000))
        t1 = int(round(time.time() * 1000))
        print("Starting Calibration")
        time.sleep(1)
        while(self.imp.cap.isOpened() and (t1-t0<10000)):
            t1,t2 = self.imp.getValue()
            gvalues1.append(t1)
            gvalues2.append(t2)
            t1 = int(round(time.time() * 1000))
        print("Calibrating ...")
        time.sleep(1)
        self.Interfaz.showMax(np.max(gvalues1),np.min(gvalues2))
        self.Interfaz.setTentative(np.max(gvalues1),np.min(gvalues2))
        T0 = int(round(time.time() * 1000))
        print("Restarting Counting ...")
        time.sleep(1)
        self.Interfaz.autoupdateThreshold()
        self.Interfaz.resetCounter()
        self.finish_function()
    
    def function_3(self):
        print("Reseting Counting")
        self.Interfaz.resetCounter()
        time.sleep(1)
        print("Counting has been reseted, please press buttom to continue")
        self.finish_function()

    def function_4(self):
        #enviar email
        self.finish_function()

    def execute(self):
        if self.state == 1:
            self.function_1()
        elif self.state == 2:
            self.function_2()
        elif self.state == 3:
            self.function_3()
        elif self.state == 4:
            self.function_4()
        self.init_machine()
        
    def init_machine(self):
        print("Iniciando Menu")
        time.sleep(2)
        self.print_menu(self.state)
        while(1):
            if self.cadena == '01' or self.cadena == '10':
                self.cadena = 'np'
                self.state = self.state%4+1
            elif self.cadena == '00' or self.cadena == '11':
                self.cadena = 'np'
                self.state = (self.state+1)%4+1
            self.print_menu(self.state)
            if self.cadena == 'p':
                self.cadena = 'np'
                break
        self.execute()