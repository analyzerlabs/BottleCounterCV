import Adafruit_CharLCD as LCD
from gpiozero import Button
from datetime import date
import RPi.GPIO as GPIO

class InterfazLCD:
    counter = 0
    serie = 0
    minT = -30
    maxT = 30
    mintentative = -36
    maxtentative = 36
    
    def __init__(self,s):
        serie = s
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        # Raspberry Pi pin configuration:
        lcd_rs        = 26  # Note this might need to be changed to 21 for older revision Pi's.
        lcd_en        = 19
        lcd_d4        = 13
        lcd_d5        = 6
        lcd_d6        = 5
        lcd_d7        = 11
        lcd_backlight = 4
        self.encoder_data     = 27
        self.encoder_clock   = 22
        encoder_buttom  = 17
        #bottom_enter  = 18

        # Define LCD column and row size for 16x2 LCD.
        lcd_columns = 16
        lcd_rows    = 2
        # Initialize the LCD using the pins above.
        self.lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)
        self.lcd.clear()
        # initialize encoder
        self.button_r = Button(encoder_buttom)
        GPIO.setup(encoder_data, GPIO.IN)
        GPIO.add_event_detect(encoder_clock, GPIO.BOTH, callback=self.encoder_interrupt)  # add rising edge detection on a channel
        GPIO.setup(encoder_clock, GPIO.IN)
        #self.button_e = Button(bottom_enter)

    def __del__(self):
        GPIO.cleanup()

    def encoder_interrupt(self):
            print("CLK Pin: ")
            print(GPIO.input(self.encoder_clock))
            print("DT Pin: ")
            print(GPIO.input(self.encoder_data))

    def showCounter(self):
        self.lcd.clear()
        self.lcd.set_cursor(0,0)
        self.lcd.message(' Bottle Counter ')
        self.lcd.set_cursor(8-len(str(self.counter)),1)
        self.lcd.message(str(self.counter))
        self.lcd.set_cursor(9,1)
        self.lcd.message('Units  ')

    def addCounter(self):
        self.counter = self.counter + 1

    def get_threshold(self):
        return (self.minT,self.maxT)

    def show_Thershold(self): 
        self.lcd.clear()
        self.lcd.set_cursor(0,0)
        self.lcd.message('minThr = ')
        self.lcd.set_cursor(10,1)
        self.lcd.message(str(self.minT))
        self.lcd.set_cursor(0,1)
        self.lcd.message('maxThr = ')
        self.lcd.set_cursor(10,1)
        self.lcd.message(str(self.maxT))

    def resetCounter(self):
        self.counter = 0;
    
    def showMax(self,val1,val2):
        self.lcd.clear()
        self.lcd.set_cursor(0,0)
        text = 'Max: ' +str(val1)
        self.lcd.message(text)
        self.lcd.set_cursor(0,1)
        text = 'Min: ' +str(val2)
        self.lcd.message(text)

    def setTentative(self,maxi,mini):
        self.maxtentative = maxi
        self.mintentative = mini

    def showTentative(self):
        self.lcd.clear()
        self.lcd.set_cursor(0,0)
        text = 'Max: ' +str(self.maxtentative)
        self.lcd.message(text)
        self.lcd.set_cursor(0,1)
        text = 'Min: ' +str(self.mintentative)
        self.lcd.message(text)

    def autoupdateThreshold(self):
        self.minT = self.mintentative*.85
        self.maxT = self.maxtentative*.85

    def menu(self):
        self.lcd.clear()
        self.lcd.set_cursor(0,0)
        self.lcd.message(' 1. Initialize ')
        self.lcd.set_cursor(0,1)
        self.lcd.message('maxThr = ')

    def save_data(self):
        today = date.today()
        file = open('data.dat','w+')
        file.write(today+'\n')
        file.close()
        

# Demo showing the cursor.

#lcd.show_cursor(True)
#lcd.message('Show cursor')

#time.sleep(5.0)

# Demo showing the blinking cursor.
#lcd.clear()
#lcd.blink(True)
#lcd.message('Blink cursor')

#time.sleep(5.0)

# Stop blinking and showing cursor.
"""lcd.show_cursor(False)
lcd.blink(False)"""