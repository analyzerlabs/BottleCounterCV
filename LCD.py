import Adafruit_CharLCD as LCD
lcd_rs        = 20  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 21
lcd_d4        = 18
lcd_d5        = 23
lcd_d6        = 24
lcd_d7        = 25
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

lcd_clear()
lcd_set_cursor(0,0)
lcd_message(' 1. Initialize ')
lcd_set_cursor(0,1)
lcd_message('maxThr = ')