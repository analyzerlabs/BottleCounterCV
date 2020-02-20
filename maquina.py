from InterfazLcd import *
from imageProcessing import *

class menu:
    lcd = InterfazLCD(1)
    imp = ImgProcessing(0)

    def __init__(self):
        self.state = 0
    
    def print_menu(self,argument):
        switcher = { 
            0: "Bottle Counter Menu", 
            1: "Start Counting", 
            2: "Calibrate Counting",
            3: "Reset Counting", 
        }
        print(switcher.get(argument, "Nothing"))
    
    def funcion_1(self):
        wait_time = 1
        found = False
        ctr = 0
        data = np.loadtxt(fname = "/home/pi/BottleCounterCV/threshold.dat")
        print ("Calibration Data: "+str(data))
        maxT=data[0]
        minT=data[1]
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
                    lcd.addCounter()
                    lcd.save_data()
                found = False
                ctr = 0
            """cv2.imshow('line',mplot)
            cv2.imshow('name',frame)"""
            #cv2.imshow('ana',img_bn)
            if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                break
