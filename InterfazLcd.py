#import Adafruit_CharLCD as LCD
from datetime import date
import datetime
import RPi.GPIO as GPIO 
import time
LCD_RS = 20
LCD_E = 21
LCD_D4 = 18
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25
LED_ON = 15

# Define some device constants

LCD_WIDTH = 0x10  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line 
# Timing constants

E_PULSE = 0.00005
E_DELAY = 0.00005
class InterfazLCD:
    counter = 0
    serie = 0
    minT = -30
    maxT = 30
    mintentative = -36
    maxtentative = 36
    
    def __init__(self,s):
        serie = s
        # DEFINIR GPIO COMO SALIDA PARA USAR LA LCD
        GPIO.setwarnings(False)

        # Initialise display

        self.lcd_init()

        # initialize encoder
        #self.button_r = Button(encoder_buttom)
    def lcd_init(self):
        GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
        GPIO.setup(LCD_E, GPIO.OUT)  # E
        GPIO.setup(LCD_RS, GPIO.OUT)  # RS
        GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
        GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
        GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
        GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
        GPIO.setup(LED_ON, GPIO.OUT)  # Backlight enable

        # Initialise display

        self.lcd_byte(0x33, LCD_CMD)
        self.lcd_byte(0x32, LCD_CMD)
        self.lcd_byte(0x28, LCD_CMD)
        self.lcd_byte(0x0C, LCD_CMD)
        self.lcd_byte(0x06, LCD_CMD)
        self.lcd_byte(0x01, LCD_CMD)

    def lcd_message(self, message, style=1,speed=1):
        # Auto splits, not perfect for clock
        # Send string to display
        # style=1 Left justified
        # style=2 Centred
        # style=3 Right justified
        # style=4 typing

        msgs = message.split('\n')
        for (idx, msg) in enumerate(msgs):
            if idx == 0:
                self.lcd_byte(LCD_LINE_1, LCD_CMD)
            elif idx == 0x01:
                self.lcd_byte(LCD_LINE_2, LCD_CMD)
            if style != 4:
                self.lcd_string(msg, style)
            elif style == 4:
                self.type_string(msg, speed)

    def type_string(self, message, speed=1, style=1):

        # Send string to display
        # style=1 Left justified
        # style=2 Centred
        # style=3 Right justified

        if style == 0x01:
            message = message.ljust(LCD_WIDTH, ' ')
        elif style == 0x02:
            message = message.center(LCD_WIDTH, ' ')
        elif style == 3:
            message = message.rjust(LCD_WIDTH, ' ')

        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)
            if message[i] != " ":
                time.sleep(speed)

    def lcd_clear(self):
        self.lcd_byte(0x06, LCD_CMD)
        self.lcd_byte(0x01, LCD_CMD)
        time.sleep(0.45)

    def write_line1(self, message, style):
        self.lcd_byte(LCD_LINE_1, LCD_CMD)
        self.lcd_string(message, style)

    def write_line2(self, message, style):
        self.lcd_byte(LCD_LINE_2, LCD_CMD)
        self.lcd_string(message, style)

    def set_line1(self):
        self.lcd_byte(LCD_LINE_1, LCD_CMD)

    def set_line2(self):
        self.lcd_byte(LCD_LINE_2, LCD_CMD)

    def lcd_string(self, message, style):
        # Send string to display
        # style=1 Left justified
        # style=2 Centred
        # style=3 Right justified

        if style == 0x01:
            message = message.ljust(LCD_WIDTH, ' ')
        elif style == 0x02:
            message = message.center(LCD_WIDTH, ' ')
        elif style == 3:
            message = message.rjust(LCD_WIDTH, ' ')

        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)

    def lcd_byte(self, bits, mode):

        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command

        GPIO.output(LCD_RS, mode)  # RS

        # High bits

        GPIO.output(LCD_D4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits & 0x10 == 0x10:
            GPIO.output(LCD_D4, True)
        if bits & 0x20 == 0x20:
            GPIO.output(LCD_D5, True)
        if bits & 0x40 == 0x40:
            GPIO.output(LCD_D6, True)
        if bits & 0x80 == 0x80:
            GPIO.output(LCD_D7, True)

            # Toggle 'Enable' pin

        time.sleep(E_DELAY)
        GPIO.output(LCD_E, True)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, False)
        time.sleep(E_DELAY)

        # Low bits

        GPIO.output(LCD_D4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits & 0x01 == 0x01:
            GPIO.output(LCD_D4, True)
        if bits & 0x02 == 0x02:
            GPIO.output(LCD_D5, True)
        if bits & 0x04 == 0x04:
            GPIO.output(LCD_D6, True)
        if bits & 0x08 == 0x08:
            GPIO.output(LCD_D7, True)

            # Toggle 'Enable' pin

        time.sleep(E_DELAY)
        GPIO.output(LCD_E, True)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, False)
        time.sleep(E_DELAY)
    
    def showCounter(self):
        self.lcd_clear()
        self.lcd_set_cursor(0,0)
        self.lcd_message(' Bottle Counter ')
        self.lcd_set_cursor(8-len(str(self.counter)),1)
        self.lcd_message(str(self.counter))
        self.lcd_set_cursor(9,1)
        self.lcd_message('Units  ')

    def addCounter(self):
        self.counter = self.counter + 1

    def get_threshold(self):
        return (self.minT,self.maxT)

    def show_Thershold(self): 
        self.lcd_clear()
        self.lcd_set_cursor(0,0)
        self.lcd_message('minThr = ')
        self.lcd_set_cursor(10,1)
        self.lcd_message(str(self.minT))
        self.lcd_set_cursor(0,1)
        self.lcd_message('maxThr = ')
        self.lcd_set_cursor(10,1)
        self.lcd_message(str(self.maxT))

    def resetCounter(self):
        self.counter = 0;
    
    def showMax(self,val1,val2):
        self.lcd_clear()
        self.lcd_set_cursor(0,0)
        text = 'Max: ' +str(val1)
        self.lcd_message(text)
        self.lcd_set_cursor(0,1)
        text = 'Min: ' +str(val2)
        self.lcd_message(text)

    def setTentative(self,maxi,mini):
        self.maxtentative = maxi
        self.mintentative = mini

    def showTentative(self):
        self.lcd_clear()
        self.lcd_set_cursor(0,0)
        text = 'Max: ' +str(self.maxtentative)
        self.lcd_message(text)
        self.lcd_set_cursor(0,1)
        text = 'Min: ' +str(self.mintentative)
        self.lcd_message(text)

    def autoupdateThreshold(self):
        
        self.minT = self.mintentative*.85
        self.maxT = self.maxtentative*.85

    def menu(self):
        self.lcd_clear()
        self.lcd_set_cursor(0,0)
        self.lcd_message(' 1. Initialize ')
        self.lcd_set_cursor(0,1)
        self.lcd_message('maxThr = ')

    def save_data(self):
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        file = open('/home/pi/BottleCounterCV/data.dat','a+')
        file.write(str(now)+'\n')
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