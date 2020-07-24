# Python script used to control motor/belt, LEDs for lighting, and camera for image acquisition. Each component
# is controlled by a self-contained function that is called when needed

import RPi.GPIO as GPIO
import picamera
import time
import board
import neopixel

detectpin = 22  # pin used for detecting button presses
motorpin = 3  # pin used with TIP120 for controlling motor
numLED = 58  # number of LEDs to be used with NeoPixel
buttonbounce = 200

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # button input = 15, motor output = 7
GPIO.setup(detectpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motorpin, GPIO.OUT)
GPIO.output(motorpin, 0)

cam = picamera.PiCamera()
cam.resolution = (3280, 2464)
cam.start_preview(fullscreen=False, window=(800, 400, 640, 480))  # draw camera preview

lights = neopixel.NeoPixel(board.D18, numLED)  # create NeoPixel object for lights
r = [[255, 197, 143], [255, 214, 170], [255, 241, 224],
     [255, 250, 244]]  # create 2D array of RGB values for common light colors


# Method for controlling motor/belt
def motor(movetime):
    GPIO.output(motorpin, 1)
    time.sleep(movetime)
    GPIO.output(motorpin, 0)
    return


# Determine amount of time required for full rotation of belt
def rotationtime():
    GPIO.add_event_detect(detectpin, GPIO.RISING, bouncetime=buttonbounce)
    while True:
        if GPIO.event_detected(detectpin):
            GPIO.output(motorpin, 0)
            GPIO.remove_event_detect(detectpin)
            break

    return


# Works with rotationtime to determine amount of time required for 360 degree rotation
def calibrate():
    GPIO.add_event_detect(detectpin, GPIO.RISING, bouncetime=buttonbounce)
    while True:
        if GPIO.event_detected(detectpin):
            GPIO.remove_event_detect(detectpin)
            GPIO.output(motorpin, 1)
            begin = time.perf_counter()
            rotationtime()
            end = time.perf_counter()
            global rotation
            rotation = end - begin  # Calculate time for full rotation for later use
            timefile = open("timefile.txt", "w")  # write rotation time to file
            timefile.write(rotation)
            break
    return


# Provides time to initiate test strip reactions and take initial photographs, if specified
def loading(clusters, strips, profile, initial):
    for i in range(clusters):
        for j in range(strips):
            GPIO.add_event_detect(detectpin, GPIO.RISING, bouncetime=buttonbounce)
            while True:
                print("Load strip, and press button when strip is securely placed on belt.")
                # User initiates chemistry, loads strip, then presses button to continue.
                if GPIO.event_detected(detectpin):
                    break
            if initial == "y":
                if profile == 1:
                    color = 0
                    for a in range(3):
                        if profile == 1:
                            lights.fill((r[color][0], r[color][1], r[color][2]))
                            cam.capture('{0}_{1}_{2}.jpg'.format(i, j, color))
                        color += 1
                else:
                    lights.fill((255, 255, 255))
                    cam.capture('{0}_{1}.jpg'.format(i, j))
            GPIO.remove_event_detect(detectpin)
            print("Motor in motion. Please prepare next strip in cluster")
            motor(rotation / strips)


if __name__ == "__main__":
    # Retrieve operation parameters from user

    print("This program was created to automate the photography of serum creatinine test strips\n\n")

    g = input("Enter the number of strip clusters (1-4):")
    n = input("Enter the number of strips per cluster (1-4):")
    p = input("Enter lighting profile to be used (1-3):")
    t = input("Enter time to wait between images (seconds):")
    f = input("Should images be obtained at t = 0? (y/n):")
    c = input("Should calibration be performed? (y/n):")

    lights.fill((255, 255, 255))  # light up all LEDs white to ease loading process

    # Initiate calibration, where time required for full rotation is calculated for later use

    print("Calibration Sequence:\n")
    print("The following calibration sequence allows for more consistency in use.\n")
    print("\t1. Place any lightweight object in the center of the viewfinder.\n")
    print("\t2. Press the push button to activate the motor. The object will rotate around the belt.\n")
    print("\t3. Once the object has traveled around the belt and is again in the center of the viewfinder, press "
          "the button again. This will record the time required for a full rotation\n")

    input("Press enter to begin calibration cycle (or skip calibration if specified)")

    if c == "y":
        calibrate()  # run calibration sequence to determine time for full rotation
    else:
        timehistory = open("timefile.txt", "r")
        rotation = float(timehistory.read())
    print("Time for full loop is " + "looptime" + "\n")

    print("Loading Sequence:")
    print("The following loading sequence allows for initiation and loading of each test strip.\n")
    print("\tFor each strip in the cluster, initiate the reaction immediately before loading the strip onto belt.")
    print("\tThis process will be repeated for each strip in the cluster, before proceeding to the next cluster.")
    print("\tIf only 1 cluster is being imaged, only one round will be made.\n")
    input("Press enter to begin loading cycle.")

    loading(g, n, p, f)  # run loading sequence and take pictures of initial strip if specified
