#
#

import RPi.GPIO as GPIO
import threading
from picamera import PiCamera
from time import sleep
import board
import neopixel


GPIO.setwarnings(False)

# button input = 15, motor output = 7
GPIO.setmode(GPIO.BOARD)

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7, GPIO.OUT)

GPIO.output(7, 0)

pixels = neopixel,NeoPixel(board.D18, x) # x = number of LEDs

print("Pins have been setup, waiting for signal to start motor operation")

def motor(timeon, timeoff, cycles, profile):
    n = cycles
    if profile == 0:
        while cycles > 0:
            a = (n - cycles) + 1
            GPIO.add_event_detect(15, GPIO.RISING)
            if GPIO.event_detected(15):
                break
            GPIO.output(7, 1)
            print("Motor in operation.")
            sleep(timeon)
            GPIO.output(7, 0)
            sleep(timeoff/2)
            cam = PiCamera()
            #cam.start_preview()
            cam.capture('/home/pi/Pictures/%s.jpg', a)
            sleep(timeoff/2)
            #cam.stop_preview()
            cycles = cycles - 1
            if cycles == 0:
                break
        print("Motor cycling complete.")

    if profile == 1:
        while cycles !=1:
            b = (n - cycles) + 1
            GPIO.add_event_detect(15, GPIO.RISING)
            # profile for

try:

    with open('config.txt', 'r') as conf:
        x = conf.read().splitlines()
    on = x[0]; off = x[1]; cyc = x[2]; prof = x[3]

    while True:
        GPIO.add_event_detect(15, GPIO.RISING)
        m = threading.Thread(target=motor, args=(on,off,cyc,prof))
        if GPIO.event_detected(15):
            m.start()
            print("Button press detected. Beginning motor cycling.")
            m.join()
            print("Cycling complete.")

except KeyboardInterrupt:
    return "Interrupt received"

finally:
    GPIO.cleanup()







