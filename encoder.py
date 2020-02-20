import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

encoder_data     = 27
encoder_clock   = 22
encoder_buttom  = 17
GPIO.setup(encoder_data, GPIO.IN)
GPIO.add_event_detect(encoder_clock, GPIO.BOTH, callback=encoder_interrupt)  # add rising edge detection on a channel
GPIO.setup(encoder_clock, GPIO.IN)

def encoder_interrupt():
    print("CLK Pin: ")
    print(GPIO.input(encoder_clock))
    print("DT Pin: ")
    print(GPIO.input(encoder_data))

try:
    while True:
        print("esperando :v")
        time.sleep(1)
except:
    GPIO.cleanup()