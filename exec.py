# Python script used to control motor/belt, LEDs for lighting, and camera for image acquisition. Each component
# is controlled by a self-contained function that is called when needed

from typing import TextIO
import os
import sys
import threading
import RPi.GPIO as GPIO # pylint: disable=import-error
import picamera # pylint: disable=import-error
import time # pylint: disable=import-error
import board # pylint: disable=import-error
import neopixel # pylint: disable=import-error
import numpy as np
import cv2

detectpin = 22  # pin used for detecting button presses
motorpin = 3  # pin used with TIP120 for controlling motor
numLED = 58  # number of LEDs to be used with NeoPixel
buttonbounce = 200  # bouncetime for GPIO button presses


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # button input = 15, motor output = 7
GPIO.setup(detectpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(motorpin, GPIO.OUT)
GPIO.output(motorpin, 0)

cam = picamera.PiCamera()
cam.resolution = (3280, 2464)
cam.start_preview(fullscreen=False, window=(800, 400, 640, 480))  # draw camera preview

def enableLights():
    lights = neopixel.NeoPixel(board.D18, numLED)  # create NeoPixel object for lights
    r = [[255, 197, 143], [255, 214, 170], [255, 241, 224],
         [255, 250, 244], [255, 255, 255]]  # create 2D array of RGB values for common light colors


# Method for activating motor/belt
def motor(movetime):
    if movetime < 0:
        return
    GPIO.output(motorpin, 1)
    time.sleep(movetime)
    GPIO.output(motorpin, 0)
    return


# Works with rotationtime to determine amount of time required for 360 degree rotation
def calibrate():
    GPIO.add_event_detect(detectpin, GPIO.RISING, bouncetime=buttonbounce)
    while True:
        if GPIO.event_detected(detectpin):
            GPIO.remove_event_detect(detectpin)
            GPIO.output(motorpin, 1)
            beginrotation: float = time.perf_counter()
            rotationtime()
            endrotation: float = time.perf_counter()
            rotation: float = endrotation - beginrotation  # Calculate time for full rotation for later use
            timefile = open("timefile.txt", "w")  # write rotation time to file
            timefile.write(str(rotation))
            break
    return rotation


# Determine amount of time required for full rotation of belt
def rotationtime():
    GPIO.add_event_detect(detectpin, GPIO.RISING, bouncetime=buttonbounce)
    while True:
        if GPIO.event_detected(detectpin):
            GPIO.output(motorpin, 0)
            GPIO.remove_event_detect(detectpin)
            break
    return


# Provides time to initiate test strip reactions and take initial photographs, if specified
def loading(clusters, initial):
    global cyclecount
    cyclecount = 1
    for i in range(clusters):
        for j in range(stripsPerCluster[i]):
            GPIO.add_event_detect(detectpin, GPIO.RISING, bouncetime=buttonbounce)
            print("Load strip, and press button when strip is securely placed on belt.")
            # User initiates chemistry, loads strip, then presses button to continue.
            while True:
                if GPIO.event_detected(detectpin):
                    break

            if initial == "y":
                if lightingCluster[i] == 1:
                    #lights.fill((255, 255, 255))
                    time.sleep(1)
                    cam.capture('{0}_{1}_{2}.jpg'.format(i, j, cyclecount))
                    # files are saved with format cluster_stripincluster_cyclecount
                elif lightingCluster[i] == 2:
                    for a in range(4):
                        lights.fill((r[a][0], r[a][1], r[a][2]))
                        time.sleep(1)
                        # filename = cluster_strip_cyclenumber_light.jpg
                        cam.capture('{0}_{1}_{2}_{3}.jpg'.format(i, j, cyclecount, a))
                elif lightingCluster[i] == 3:
                    for a in range(5):
                        #lights.fill((r[a][0], r[a][1], r[a][2]))
                        time.sleep(1)
                        cam.capture('{0}_{1}_{2}_{3}.jpg'.format(i, j, cyclecount, a))
                else:
                    print("Starting image was requested, but valid lighting profile was not specified."
                          + "Defaulting to white light.\n")
                    #lights.fill((255, 255, 255))
                    time.sleep(1)
                    cam.capture('{0}_{1}_{2}.jpg'.format(i, j, cyclecount))

            GPIO.remove_event_detect(detectpin)
            print("Motor in motion. Please prepare next strip in cluster")
            if (j + 1 == stripsPerCluster[i]) and (i + 1 == clusters):
                clusterOffset = rot_time / (stripsPerCluster[i] * clusters)
                motor(clusterOffset)
            else:
                motor(rot_time / stripsPerCluster[i])
        offset = getCorrection()
        correct(offset)
        if i + 1 == clusters:
            continue
        else:
            clusterOffset = rot_time / (stripsPerCluster[i] * clusters)
            motor(clusterOffset)
    if initial == "y":
        cyclecount += 1
    return


# Cycling of belt, similar to loading cycle but without user confirmation (automated)
def cycling():
    global cyclecount
    global shouldAdjust
    for i in range(g):
        for j in range(stripsPerCluster[i]):
            if lightingCluster[i] == 1:
                #lights.fill((255, 255, 255))
                time.sleep(1)
                cam.capture('{0}_{1}_{2}.jpg'.format(i, j, cyclecount))
            elif lightingCluster[i] == 2:
                for a in range(4):
                    #lights.fill((r[a][0], r[a][1], r[a][2]))
                    time.sleep(1)
                    # filename = cluster_strip_light.jpg
                    cam.capture('{0}_{1}_{2}_{3}.jpg'.format(i, j, a, cyclecount))
            elif lightingCluster[i] == 3:
                for a in range(5):
                    #lights.fill((r[a][0], r[a][1], r[a][2]))
                    time.sleep(1)
                    cam.capture('{0}_{1}_{2}_{3}.jpg'.format(i, j, cyclecount, a))


            if (j + 1 == stripsPerCluster[i]) and (i + 1 == g):
                if shouldAdjust == 0:
                    clusterOffset = rot_time / (stripsPerCluster[i] * g)
                    motor(clusterOffset)
                elif shouldAdjust != 0:
                    clusterOffset = rot_time / (stripsPerCluster[i] * g) - shouldAdjust
                    motor(clusterOffset)
                    shouldAdjust = 0
            elif (j + 1 == stripsPerCluster[i]) and (i + 1 != g):
                motor(rot_time / stripsPerCluster[i])
                offset = getCorrection()
                correct(offset)
                clusterOffset = rot_time / (stripsPerCluster[i] * g)
                motor(clusterOffset)
            else:
                motor(rot_time / stripsPerCluster[i])
            """
            if shouldAdjust == 0:
                motor(rot_time / stripsPerCluster[i])
            elif shouldAdjust != 0:
                motor(rot_time / (stripsPerCluster[i] * g) - shouldAdjust)
                shouldAdjust = 0
            """
        """
        offset = getCorrection()
        correct(offset)
        """
    """
        if i + 1 == g:
            continue
        else:
            clusterOffset = rot_time / (stripsPerCluster[i] * g)
            motor(clusterOffset)
    """
    cyclecount += 1
    return

def getCorrection():
    checkX = [142, 171, 199, 242, 284, 324, 370, 413, 461, 511, 558, 604, 652, 705, 752, 804, 856, 907, 960, 1012]
    checkY = [520, 497, 476, 440, 413, 388, 365, 345, 330, 317, 309, 298, 293, 290, 284, 286, 295, 298, 311, 323]
    boundaries = ([150,30,30],[255,255,255])
    cam.resolution = (1280, 720)

    cam.capture('correction.jpg')
    image = cv2.imread("correction.jpg")

    lower = np.array(boundaries[0], dtype = "uint8")
    upper = np.array(boundaries[1], dtype = "uint8")

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    """
    # lists of x and y coordinates that tell program where to look for blue sticker
    checkX = [142, 171, 199, 242, 284, 324, 370, 413, 461, 511, 558, 604, 652, 705, 752, 804, 856, 907, 960, 1012]
    checkY = [520, 497, 476, 440, 413, 388, 365, 345, 330, 317, 309, 298, 293, 290, 284, 286, 295, 298, 311, 323]
    # x = 717, y = 293
    # output[y][x]
    """

    #check all predefined locations for sticker to determine where strip is
    for spotCheck in range(20):
        if np.any(output[checkY[spotCheck]][checkX[spotCheck]] != False):
            print("Belt in position " + str(spotCheck))
            return spotCheck
        else:
            continue
    cam.resolution = (3280, 2464)
    return


    #cv2.imwrite("correctionOut.jpg", output)

def correct(location):
    if location == 13:
        return
    if 0 <= location < 13:
        motor((7.7)*((13-location)/13))
        return
    elif 13 < location <= 19:
        #global shouldAdjust
        shouldAdjust = ((19-location)/6)*3.5
        return
    else:
        return


# Program starts here unless imported
if __name__ == "__main__":
    # Retrieve operation parameters from user
    print("This program was created to automate the photography of diagnostic test strips.\n\n")

    while True:
        g = int(input("Enter the number of strip clusters (1-2)..."))
        if 1 <= g <= 2:
            break

    stripsPerCluster = []
    while True:
        for cluster in range(g):
            while True:
                n = int(input("Enter the number of strips in cluster " + str(cluster) + "\n"))
                if 1 <= n <= 4:
                    stripsPerCluster.append(n)
                    break
                else:
                    continue


        if len(stripsPerCluster) == g:
            print(stripsPerCluster)
            print("\n")
            confirmation = input("Is this the correct number of strips in each cluster?")
            if confirmation == "n":
                continue
            else:
                break

    lightingCluster = []
    while True:
        for cluster in range(g):
            while True:
                p = int(input("Enter the lighting profile to be used for cluster" + str(cluster) + "\n"))
                if 1 <= p <= 2:
                    lightingCluster.append(p)
                    break

        # p = int(input("Enter lighting profile to be used (1-3)..."))  # 1 = white light, 2 = 4 colors
        # support for multiple colors coming later, profiles should all be 1
        if len(lightingCluster) == g:
            print(lightingCluster)
            confirmation = input("Is this the correct lighting profile for each cluster?")
            if confirmation == "n":
                continue
            else:
                break

    while True:
        t = int(input("Enter time to wait between images (seconds)..."))
        if t > 80:
            break
    while True:
        f = str(input("Should images be obtained at t = 0? (y/n)..."))
        if f == 'y' or f == 'n':
            break
    while True:
        c = str(input("Should calibration be performed? (y/n)..."))
        if c == 'y' or c == 'n':
            break
    while True:
        e = int(input("Enter number of cycles to perform..."))
        if e >= 0:
            break

    # light up all LEDs white to ease loading process
    #enableLights()
    #lights.fill((255, 255, 255))

    # Initiate calibration, where time required for full rotation is calculated for later use
    print("Calibration Sequence:\n\n"
          + "The following calibration sequence allows for more consistency in use.\n\n"
          + "1. Place any lightweight object in the center of the viewfinder.\n\n"
          + "2. Press the push button to activate the motor. The object will rotate around the belt.\n\n"
          + "3. Once the object has traveled around the belt and is again in the center of the viewfinder, press "
          + "the button again. This will record the time required for a full rotation\n\n")

    input("Press enter to begin calibration cycle (or skip calibration if specified)...")

    if c == "y":
        rot_time: float = calibrate()  # run calibration sequence to determine time for full rotation
    elif c == "n":
        try:
            timehistory: TextIO = open("timefile.txt", "r")
            rot_time: float = float(timehistory.read())
        except:
            raise

    print("Time for full loop is {0}.\n".format(str(rot_time)))

    print("Loading Sequence:\n\n"
          + "The following loading sequence allows for initiation and loading of each test strip.\n\n"
          + "For each strip in the cluster, initiate the reaction immediately before loading the strip onto belt."
          + "This process will be repeated for each strip in the cluster, before proceeding to the next cluster."
          + "If only 1 cluster is being imaged, only one round will be made.\n\n")

    cyclecount = 0
    input("Press enter to begin loading cycle...\n")

    beginloading: float = time.perf_counter()
    loading(g, f)  # run loading sequence and take pictures of initial strip if specified
    endloading: float = time.perf_counter()
    loadingtime: float = endloading - beginloading
    tracker: float = t - loadingtime


    shouldAdjust = 0
    while cyclecount <= e:
        cyclethread = threading.Timer(tracker, cycling)
        begincycle: float = time.perf_counter()
        cyclethread.start()
        print("Performing photo cycle. Please wait.")
        cyclethread.join()
        endcycle: float = time.perf_counter()
        tracker = t - (endcycle - begincycle)
        print("Waiting for next photo cycle.")

    print("Process complete. All cycles have been completed.\n")
    print("Images are saved in current directory")
    sys.exit(0)
