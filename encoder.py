import RPi.GPIO as GPIO
import time

encoder_data     = 27
encoder_clock   = 22
encoder_buttom  = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def encoder_interrupt(channel):
    print("CLK,DT "+str(GPIO.input(encoder_clock))+","+str(GPIO.input(encoder_data)))

GPIO.setup(encoder_clock, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(encoder_data, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(encoder_clock, GPIO.BOTH, callback=encoder_interrupt)  # add rising edge detection on a channel

try:
    while True:
        time.sleep(1)
finally:
    GPIO.cleanup()