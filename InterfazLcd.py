import Adafruit_CharLCD as LCD

class LCD:
    counter = 0
    def __init__(self):
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
        self.lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
                                lcd_columns, lcd_rows, lcd_backlight)
        self.lcd.clear()
    def menu(self):
        return 0
    
    def showCounter(self):
        lcd.clear()
        lcd.set_cursor(0,0)
        lcd.message(' Bottle Counter ')
        lcd.set_cursor(10-len(str(counter)),1)
        lcd.message(str(counter))
        lcd.set_cursor(11,1)
        lcd.message('Units ')


    def addCounter(self):
        counter = counter + 1
        

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