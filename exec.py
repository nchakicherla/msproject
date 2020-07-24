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

# Method for controlling motor/belt

def motor():

# Method for determining how long it takes for full rotation of belt

def rotationtime():
    while True:
        if GPIO.event_detected(detectpin):
            GPIO.output(motorpin, 0)
            break
    return

def calibrate():
    GPIO.add_event_detect(detectpin, GPIO.RISING, bouncetime=500)
    if GPIO.event_detected(detectpin):
        GPIO.output(motorpin, 1)
        begin = time.perf_counter()
        rotationtime()
        end = time.perf_counter()
        looptime = end - begin # Calculate time for full rotation for later use


# Retrieve operation parameters from user

g = input("Enter the number of strip groups (1-4):")
n = input("Enter the number of strips per group (1-4):")
i = input("Enter lighting profile to be used:")
t = input("Enter time to wait between images (seconds):")
f = input("Should images be obtained at t = 0? (y/n):")

# Start with loading cycle, where reactions are initiated and strips are loaded onto belt

lights = neopixel.NeoPixel(board.D18, numLED)
lights.fill((255, 255, 255)) # light up all LEDs white to ease loading process









