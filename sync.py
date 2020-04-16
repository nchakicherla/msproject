#
#

import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep

GPIO.setwarnings(False)

# button input = 15, motor output = 7
GPIO.setmode(GPIO.BOARD)

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7, GPIO.OUT)

GPIO.output(7, 0)

def (15, timeon, timeoff, cycles):
    print("Button pressed! Motor in operation.")
    n = cycles
    while cycles != 0:
        a = (n - cycles) + 1
        GPIO.add_event_detect(15, GPIO.RISING)
        GPIO.output(7, 1)
        sleep(timeon)
        GPIO.output(7, 0)
        cam = PiCamera()
        camera.start_preview()
        camera.capture('/home/pi/Pictures/%s.jpg', a)
        sleep(timeoff)
        camera.stop_preview()
        if GPIO.event_detected(15):
            break
        cycles = cycles - 1
    return "Motor cycling complete."
try
    while True:
        GPIO.add_event_detect(15, GPIO.RISING, callback=motor)
        timeon = 1
        timeoff = 1
        cycles = 8
except KeyboardInterrupt:
    print("Interrupt received.")
    return





