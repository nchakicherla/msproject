def motor(time):
    # import GPIO module for use of pins
    import RPi.GPIO as GPIO
    from time import sleep

    # set mode to use BOARD numbering
    GPIO.setmode(GPIO.BOARD)

    # designate each pin as input/output and initial values
    GPIO.setup(3, GPIO.OUT)                             # output pin for control of motor via TIP120 base (GPIO2)
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # input pin for button input, pulled down to provide discrete signal (GPIO14)
    
    try:
        while True:
            if GPIO.input(8):
                print("Input pin 8 is HIGH - Output pin 2 is HIGH")
                GPIO.output(3, 1)       # set pin 3 output to HIGH/1
            else:
                print("Input pin 8 is LOW - Output pin 2 is LOW")
                GPIO.output(3, 0)       # set pin 3 output to LOW/0
            sleep(time)                 # wait for certain amount of time from argument

    except:
        print("An exception occurred")  # if code is unsuccessful return error message
        
    finally:
        GPIO.cleanup()                  # revert settings to prevent damage to GPIO and RPi
