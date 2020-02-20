import RPi.GPIO as GPIO
import time

encoder_data     = 27
encoder_clock   = 22
encoder_buttom  = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(encoder_clock, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder_data, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(encoder_clock, GPIO.BOTH, callback=encoder_interrupt)  # add rising edge detection on a channel

def encoder_interrupt():
    print("CLK,DT "+str(GPIO.input(encoder_clock))+","+str(GPIO.input(encoder_data)))

try:
    while True:
        time.sleep(1)
finally:
    GPIO.cleanup()