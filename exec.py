# Python script used to control motor/belt, LEDs for lighting, and camera for image acquisition. Each component
# is controlled by a self-contained function that is called whenever needed.

import RPi.GPIO as GPIO
import threading
from picamera import PiCamera
from time import sleep
import board
import neopixel

detectpin = 22
proceedpin = 27
motorpin = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # button input = 15, motor output = 7
GPIO.setup(detectpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motorpin, GPIO.OUT)
GPIO.output(motorpin, 0)

# Method for controlling motor/belt

def motor():

# Retrieve operation parameters from user

g = input("Enter the number of strip groups (1-4):")
n = input("Enter the number of strips per group (1-4):")
i = input("Enter lighting profile to be used:")
t = input("Enter time to wait between images (seconds):")
f = input("Should images be obtained at t = 0? (y/n):")









