class syncBelt:
    
    def __init__(self, interval, duration):
        self.interval = interval
        self.duration = duration
        
    def motor(self):
        
        # import RPi.GPIO module for using of pins
        import RPi.GPIO as GPIO
        from time import sleep

        # set mode to use BOARD numbering
        GPIO.setmode(GPIO.BOARD)

        # designate each pin as input/output and initial values
        GPIO.setup(3, GPIO.OUT)                             # output pin for control of motor via TIP120 base lead (GPIO2)
        GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # input pin for button input, pulled down to provide discrete signal (GPIO14)
        
        try:
            while duration != 0:
                if GPIO.input(8):
                    print("Input pin 8 is HIGH - Output pin 2 is HIGH")
                    GPIO.output(3, 1)           # set pin 3 output to HIGH/1
                else:
                    print("Input pin 8 is LOW - Output pin 2 is LOW")
                    GPIO.output(3, 0)           # set pin 3 output to LOW/0
                sleep(interval)                 # wait for specified amount of time before repolling (s)
                duration = duration - interval  # iterate duration downwards by interval (s) until duration is 0
                

        except:
            print("An exception occurred (motor)")  # if code is unsuccessful return error message
            
        finally:
            GPIO.cleanup()                  # revert settings to prevent damage to GPIO and RPi

    def camera(self):

        # import RPi.GPIO module for using pins
        import RPi.GPIO as GPIO
        
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # input pin for button input, different button with but connected to same 3v3 power pin 1

        try:
            if GPIO.input(12):
                print("Input pin 12 is HIGH - trigger camera")
                GPIO.output(7, 1)           # set pin 7 output to HIGH/1, trigger camera
            else:
                print("Input pin 12 is LOW - don't trigger camera")
                GPIO.output(7, 0)           # set pin 7 output to LOW/0

        except:
            print("An exception occurred (camera)")

        finally:
            GPIO.cleanup()

    def light(self):

        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # using same input pin as camera button, camera will trigger once every light change (6 times)

        try:
            if GPIO.input(12):
                print("Input pin 12 is HIGH - trigger lighting change")
                GPIO.output(11, 1)          # set pin 11 output to HIGH/1, trigger light change
            else:
                print("Input pin 12 is LOW - don't trigger lighting change")
                GPIO.output(11, 0)          # set pin 11 output to LOW/0, do not trigger light change

        except:
            print("An exception occurred (light)")

        finally:
            GPIO.cleanup()
            
    
