# Python script used to control motor/belt, LEDs for lighting, and camera for image acquisition. Each component
# is controlled by a self-contained function that is called whenever needed.

import RPi.GPIO as GPIO
import threading
from picamera import PiCamera
import time
import board
import neopixel

detectpin = 22 # pin used for detecting button presses
motorpin = 3 # pin used with TIP120 for controlling motor
numLED = 58 # number of LEDs to be used with NeoPixel

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # button input = 15, motor output = 7
GPIO.setup(detectpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motorpin, GPIO.OUT)
GPIO.output(motorpin, 0)

cam = picamera.PiCamera()
cam.resolution = (3280,2464)
cam.start_preview(fullscreen = False, window = (800, 400, 640, 480)) # draw camera preview

# Method for controlling motor/belt

def motor():
    return

# Method for determining how long it takes for full rotation of belt

def rotationtime():
    while True:
        GPIO.add_event_detect(detectpin, GPIO.RISING, bouncetime=200)
        if GPIO.event_detected(detectpin):
            GPIO.output(motorpin, 0)
            break
        GPIO.remove_event_detect(detectpin)
    return

def calibrate():
    GPIO.add_event_detect(detectpin, GPIO.RISING, bouncetime=200)
    while True:
        if GPIO.event_detected(detectpin):
            GPIO.output(motorpin, 1)
            begin = time.perf_counter()
            GPIO.remove_event_detect(detectpin)
            rotationtime()
            end = time.perf_counter()
            global looptime
            looptime = end - begin # Calculate time for full rotation for later use
            break
    return


# Retrieve operation parameters from user

print("This program was created to automate the photography of serum creatinine test strips\n\n")

g = input("Enter the number of strip groups (1-4):")
n = input("Enter the number of strips per group (1-4):")
i = input("Enter lighting profile to be used :")
t = input("Enter time to wait between images (seconds):")
f = input("Should images be obtained at t = 0? (y/n):")

lights = neopixel.NeoPixel(board.D18, numLED)
lights.fill((255, 255, 255)) # light up all LEDs white to ease loading process


# Initiate calibration, where time required for full rotation is calculated for later use

print("Calibration Sequence:")
print("The following calibration sequence allows for more consistency in use\n")
print("1. Place any lightweight object in the center of the viewfinder.\n")
print("2. Press the push button to activate the motor. The object will rotate around the belt.\n")
print("3. Once the object has traveled around the belt and is again in the center of the viewfinder,")
print("\tpress the button again. This will record the time required for a full rotation\n")

input("Press enter to continue...")

calibrate()













