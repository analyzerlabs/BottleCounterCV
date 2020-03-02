#import Adafruit_CharLCD as LCD
from datetime import date
import datetime
import RPi.GPIO as GPIO 
import time

class InterfazLCD:
    counter = 0
    serie = 0
    minT = -30
    maxT = 30
    mintentative = -36
    maxtentative = 36
    GPIO.cleanup()
    # DEFINICIONES PARA ASIGNACION DE PINES
    LCD_CLEARDISPLAY        = 0x01
    LCD_RETURNHOME          = 0x02
    LCD_ENTRYMODESET        = 0x04
    LCD_DISPLAYCONTROL      = 0x08
    LCD_CURSORSHIFT         = 0x10
    LCD_FUNCTIONSET         = 0x20
    LCD_SETCGRAMADDR        = 0x40
    LCD_SETDDRAMADDR        = 0x80
    # Entry flags
    LCD_ENTRYRIGHT          = 0x00
    LCD_ENTRYLEFT           = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00
    # Control flags
    LCD_DISPLAYON           = 0x04
    LCD_DISPLAYOFF          = 0x00
    LCD_CURSORON            = 0x02
    LCD_CURSOROFF           = 0x00
    LCD_BLINKON             = 0x01
    LCD_BLINKOFF            = 0x00
    # Move flags
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00
    LCD_MOVERIGHT           = 0x04
    LCD_MOVELEFT            = 0x00
    # Function set flags
    LCD_8BITMODE            = 0x10
    LCD_4BITMODE            = 0x00
    LCD_2LINE               = 0x08
    LCD_1LINE               = 0x00
    LCD_5x10DOTS            = 0x04
    LCD_5x8DOTS             = 0x00
    # Offset for up to 4 rows.
    LCD_ROW_OFFSETS         = (0x00, 0x40, 0x14, 0x54)
    # Char LCD plate GPIO numbers.
    LCD_PLATE_RS            = 15
    LCD_PLATE_RW            = 14
    LCD_PLATE_EN            = 13
    LCD_PLATE_D4            = 12
    LCD_PLATE_D5            = 11
    LCD_PLATE_D6            = 10
    LCD_PLATE_D7            = 9
    LCD_PLATE_RED           = 6
    LCD_PLATE_GREEN         = 7
    LCD_PLATE_BLUE          = 8
    # Char LCD plate button names.
    SELECT                  = 0
    RIGHT                   = 1
    DOWN                    = 2
    UP                      = 3
    LEFT                    = 4
    # Char LCD backpack GPIO numbers.
    LCD_BACKPACK_RS         = 1
    LCD_BACKPACK_EN         = 2
    LCD_BACKPACK_D4         = 3
    LCD_BACKPACK_D5         = 4
    LCD_BACKPACK_D6         = 5
    LCD_BACKPACK_D7         = 6
    LCD_BACKPACK_LITE       = 7

    def __init__(self,s):
        serie = s
        # DEFINIR GPIO COMO SALIDA PARA USAR LA LCD
        GPIO.setmode(GPIO.BCM) # USAR LA NOMENCLATURA BCM (HARDWARE)
        GPIO.setwarnings(False)
        self.lcd_init(20,21,18,23,24,25,16,2)

        # initialize encoder
        #self.button_r = Button(encoder_buttom)
    def lcd_init(self, rs, en, d4, d5, d6, d7, cols, lines, backlight=None):
        self._cols = cols
        self._lines = lines
        # Save GPIO state and pin numberS
        self._rs = rs
        self._en = en
        self._d4 = d4
        self._d5 = d5
        self._d6 = d6
        self._d7 = d7
        for pin in (rs, en, d4, d5, d6, d7):
            GPIO.setup(pin, GPIO.OUT)
         # Initialize the display.
        self.write8(0x33)
        self.write8(0x32)
        # Initialize display control, function, and mode registers.
        self.displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_2LINE | LCD_5x8DOTS
        self.displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        # Write registers.
        self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)
        self.write8(LCD_FUNCTIONSET | self.displayfunction)
        self.write8(LCD_ENTRYMODESET | self.displaymode)  # set the entry mode
        self.lcd_clear()

    def lcd_clear(self):
        self.write8(self.LCD_CLEARDISPLAY)  # command to clear display
        self._delay_microseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

    def lcd_set_cursor(self, col, row):
        """Move the cursor to an explicit column and row position."""
        # Clamp row to the last row of the display.
        if row > self._lines:
            row = self._lines - 1
        # Set location.
        self.write8(self.LCD_SETDDRAMADDR | (col + self.LCD_ROW_OFFSETS[row]))

    def enable_display(self, enable):
        """Enable or disable the display.  Set enable to True to enable."""
        if enable:
            self.displaycontrol |= self.LCD_DISPLAYON
        else:
            self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write8(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def show_cursor(self, show):
        """Show or hide the cursor.  Cursor is shown if show is True."""
        if show:
            self.displaycontrol |= self.LCD_CURSORON
        else:
            self.displaycontrol &= ~self.LCD_CURSORON
        self.write8(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def blink(self, blink):
        """Turn on or off cursor blinking.  Set blink to True to enable blinking."""
        if blink:
            self.displaycontrol |= self.LCD_BLINKON
        else:
            self.displaycontrol &= ~self.LCD_BLINKON
        self.write8(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def move_left(self):
        """Move display left one position."""
        self.write8(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def move_right(self):
        """Move display right one position."""
        self.write8(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)

    def set_left_to_right(self):
        """Set text direction left to right."""
        self.displaymode |= self.LCD_ENTRYLEFT
        self.write8(self.LCD_ENTRYMODESET | self.displaymode)

    def set_right_to_left(self):
        """Set text direction right to left."""
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.write8(self.LCD_ENTRYMODESET | self.displaymode)

    def autoscroll(self, autoscroll):
        """Autoscroll will 'right justify' text from the cursor if set True,
        otherwise it will 'left justify' the text.
        """
        if autoscroll:
            self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        else:
            self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.write8(self.LCD_ENTRYMODESET | self.displaymode)

    def message(self, text):
        """Write text to display.  Note that text can include newlines."""
        line = 0
        # Iterate through each character.
        for char in text:
            # Advance to next line if character is a new line.
            if char == '\n':
                line += 1
                # Move to left or right side depending on text direction.
                col = 0 if self.displaymode & self.LCD_ENTRYLEFT > 0 else self._cols-1
                self.set_cursor(col, line)
            # Write the character to the display.
            else:
                self.write8(ord(char), True)

    def write8(self, value, char_mode=False):
        """Write 8-bit value in character or data mode.  Value should be an int
        value from 0-255, and char_mode is True if character data or False if
        non-character data (default).
        """
        # One millisecond delay to prevent writing too quickly.
        self._delay_microseconds(1000)
        # Set character / data bit.
        GPIO.output(self._rs, char_mode)
        # Write upper 4 bits.
        GPIO.output(self._d4, ((value >> 4) & 1) > 0)
        GPIO.output(self._d5, ((value >> 5) & 1) > 0)
        GPIO.output(self._d6, ((value >> 6) & 1) > 0)
        GPIO.output(self._d7, ((value >> 7) & 1) > 0)
        self._pulse_enable()
        # Write lower 4 bits.
        GPIO.output(self._d4, (value        & 1) > 0)
        GPIO.output(self._d5, ((value >> 1) & 1) > 0)
        GPIO.output(self._d6, ((value >> 2) & 1) > 0)
        GPIO.output(self._d7, ((value >> 3) & 1) > 0 )
        self._pulse_enable()
    def _pulse_enable(self):
        # Pulse the clock enable line off, on, off to send command.
        self._gpio.output(self._en, False)
        self._delay_microseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
        self._gpio.output(self._en, True)
        self._delay_microseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
        self._gpio.output(self._en, False)
        self._delay_microseconds(1)       # commands need > 37us to settle
        
    def create_char(self, location, pattern):
        """Fill one of the first 8 CGRAM locations with custom characters.
        The location parameter should be between 0 and 7 and pattern should
        provide an array of 8 bytes containing the pattern. E.g. you can easyly
        design your custom character at http://www.quinapalus.com/hd44780udg.html
        To show your custom character use eg. lcd.message('\x01')
        """
        # only position 0..7 are allowed
        location &= 0x7
        self.write8(self.LCD_SETCGRAMADDR | (location << 3))
        for i in range(8):
            self.write8(pattern[i], char_mode=True)

    def _delay_microseconds(self, microseconds):
        # Busy wait in loop because delays are generally very short (few microseconds).
        end = time.time() + (microseconds/1000000.0)
        while time.time() < end:
            pass
    
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
        self.lcd.clear()
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
        self.lcd.clear()
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
        self.lcd.clear()
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
        self.lcd.clear()
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