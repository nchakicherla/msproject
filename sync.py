#
#

import RPi.GPIO as GPIO
from picamera import PiCamera
import board
import neopixel
from time import sleep

GPIO.setwarnings(False)

# button input = 15, motor output = 7
GPIO.setmode(GPIO.BOARD)

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7, GPIO.OUT)

GPIO.output(7, 0)

pixels = neopixel,NeoPixel(board.D18, x) # x = number of LEDs

print("Pins have been setup, waiting for signal to start motor operation")

def motor(timeon, timeoff, cycles, profile):
    print("Button pressed! Motor in operation.")
    n = cycles
    if profile == 0:
        while cycles != 1:
            a = (n - cycles) + 1
            GPIO.add_event_detect(15, GPIO.RISING)
            if GPIO.event_detected(15):
                break
            GPIO.output(7, 1)
            sleep(timeon)
            GPIO.output(7, 0)
            sleep(timeoff/2)
            cam = PiCamera()
            camera.start_preview()
            camera.capture('/home/pi/Pictures/%s.jpg', a)
            sleep(timeoff/2)
            camera.stop_preview()
            cycles = cycles - 1
            if cycles == 0:
                break
        print("Motor cycling complete.")

    if profile == 1:
        while cycles !=1:
            b = (n - cycles) + 1
            GPIO.add_event_detect(15, GPIO.RISING)


try:

    GPIO.add_event_detect(15, GPIO.RISING)
    on = 1
    off = 1
    cyc = 8
    prof = 1
    if GPIO.event_detected(15):
        motor(on, off, cyc, prof)


except KeyboardInterrupt:
    print("Interrupt received. Program exited")





