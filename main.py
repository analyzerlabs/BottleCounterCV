import numpy as np
#import cv2
from maquina import *
#import matplotlib.pyplot as plt

print("Creando objetos")
mch = maquina()
print("Maquina iniciada")
mch.init_machine()
print("Maquina Finalizada")
"""wait_time = 1

lcd= InterfazLCD(1)
imp = ImgProcessing(0)
found = False
ctr = 0
T0 = int(round(time.time() * 1000))
data = np.loadtxt(fname = "/home/pi/BottleCounterCV/threshold.dat")
print (data)
maxT=data[0]
minT=data[1]
state = 0   #state 0 main menu
# used to get value of max gradient
getgradient = False
gvalues1 = []
gvalues2 = []
firstCalibration = True
while(imp.cap.isOpened()):
    t1,t2 = imp.getValue()
    minT,maxT = lcd.get_threshold()
    if t1 > maxT or t2 < minT:
        found = True
        ctr = 0
        
    else:
        ctr = ctr + 1
    if ctr == 8:
        if found: 
            #print("found prr")
            lcd.addCounter()
            lcd.save_data()
        found = False
        ctr = 0
    cv2.imshow('line',mplot)
    cv2.imshow('name',frame)
    #cv2.imshow('ana',img_bn)
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        break

    T1 = int(round(time.time() * 1000))
    # if reset boton is pressed
    if lcd.button_r.is_pressed or firstCalibration:
        print("entre prr")
        firstCalibration = False
        getgradient = True
        gvalues1 = []
        gvalues2 = []
        temp0 = int(round(time.time() * 1000))
        #lcd.button_r.when_released = lcd.resetCounter()
    # if getgradient is actived
    if getgradient and (T1-temp0<10000):
        gvalues1.append(t1)
        gvalues2.append(t2)
        print(t1,t2)
    else:
        if getgradient:
            lcd.showMax(np.max(gvalues1),np.min(gvalues2))
            lcd.setTentative(np.max(gvalues1),np.min(gvalues2))
            T0 = int(round(time.time() * 1000))
            lcd.autoupdateThreshold()
            lcd.resetCounter()
        getgradient = False
        
    # update display on lcd
    if(T1-T0>=1000):
        T0 = T1
        lcd.showCounter()
        print(lcd.counter)

imp.cap.release()
cv2.destroyAllWindows()"""

