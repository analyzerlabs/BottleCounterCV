import numpy as np
#import cv2
import time
from InterfazLcd import *
from imageProcessing import *
#import matplotlib.pyplot as plt

wait_time = 1

lcd= InterfazLCD(1)
imp = ImgProcessing(0)
found = False
ctr = 0
T0 = int(round(time.time() * 1000))
data = np.load("threshold.dat")
maxT=data[0]
minT=data[1]
# used to get value of max gradient
getgradient = False
gvalues1 = []
gvalues2 = []
while(imp.cap.isOpened()):
    """# update data
    ret,frame = cap.read()
    img_bn = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    v = img_bn.shape[0]
    h = img_bn.shape[1]
    #print(h,v)
    d1 = int(0.2*v/2)
    d2 = int(1.8*v/2)
    w1 = int(0.2*h)
    w2 = int(0.8*h)
    cv2.rectangle(frame,(w1,d1),(w2,d2),(0,255,0),1)
    # getting region
    img_bn = cv2.resize(img_bn,(int(h/10),int(v/10)),interpolation = cv2.INTER_AREA)
    img_bn = cv2.GaussianBlur(img_bn,(5,5),0)
    v = img_bn.shape[0]
    h = img_bn.shape[1]
    #print(h,v)
    d1 = int(0.6*v/2)
    d2 = int(1.4*v/2)
    w1 = int(0.2*h)
    w2 = int(0.8*h)
    img_bn = img_bn[d1:d2,w1:w2]
    obj = np.mean(img_bn, axis=1)
    dobj = np.convolve(obj, [5, -5], 'valid')*5

    # drawing
    retval = cv2.plot.Plot2d_create(dobj)
    retval.setMaxY(100)
    retval.setMinY(-100)
    mplot = retval.render()
    # analisis
    t1 = np.max(dobj)
    t2 = np.min(dobj)"""
    t1,t2 = imp.getValue()
    minT,maxT = lcd.get_threshold()
    if t1 > maxT or t2 < minT:
        found = True
        ctr = 0
        """print(t1)
        print(t2)"""
        
    else:
        ctr = ctr + 1
    if ctr == 8:
        if found: 
            #print("found prr")
            lcd.addCounter()
        found = False
        ctr = 0
    """cv2.imshow('line',mplot)
    cv2.imshow('name',frame)"""
    #cv2.imshow('ana',img_bn)
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        break

    T1 = int(round(time.time() * 1000))
    # if reset boton is pressed
    if lcd.button_r.is_pressed:
        print("entre prr")
        getgradient = True
        gvalues1 = []
        gvalues2 = []
        temp0 = int(round(time.time() * 1000))
        #lcd.button_r.when_released = lcd.resetCounter()
    # if getgradient is actived
    if getgradient and (T1-temp0<5000):
        gvalues1.append(t1)
        gvalues2.append(t2)
        print(t1,t2)
    else:
        if getgradient:
            lcd.showMax(np.max(gvalues1),np.min(gvalues2))
            lcd.setTentative(np.max(gvalues1),np.min(gvalues2))
            T0 = int(round(time.time() * 1000))
            lcd.autoupdateThreshold()
        getgradient = False
        
    # update display on lcd
    if(T1-T0>=2000):
        T0 = T1
        lcd.showCounter()
        print(lcd.counter)

imp.cap.release()
cv2.destroyAllWindows()