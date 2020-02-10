import Adafruit_CharLCD as LCD

class InterfazLCD:
    counter = 0
    serie = 0
    minT = -30
    maxT = 30
    def __init__(self,s):
        serie = s
        # Raspberry Pi pin configuration:
        lcd_rs        = 27  # Note this might need to be changed to 21 for older revision Pi's.
        lcd_en        = 22
        lcd_d4        = 25
        lcd_d5        = 24
        lcd_d6        = 23
        lcd_d7        = 18
        lcd_backlight = 4
        # Define LCD column and row size for 16x2 LCD.
        lcd_columns = 16
        lcd_rows    = 2
        # Initialize the LCD using the pins above.
        self.lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)
        self.lcd.clear()

    def showCounter(self):
        self.lcd.clear()
        self.lcd.set_cursor(0,0)
        self.lcd.message(' Bottle Counter ')
        self.lcd.set_cursor(10-len(str(self.counter)),1)
        self.lcd.message(str(self.counter))
        self.lcd.set_cursor(11,1)
        self.lcd.message('Units ')


    def addCounter(self):
        self.counter = self.counter + 1

    def lcd.get_Threshold(self):
        return (self.minT,self.maxT)
    
        

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