class syncBelt:
    import RPi.GPIO as GPIO
    from time import sleep
    
    def __init__(self, duration, timeon, timeoff):
        self.duration = duration
        self.timeon = timeon
        self.timeoff = timeoff
        # duration should be an integer multiple of interval (s)
        
    def motor(self):
        
        GPIO.cleanup()
        
        # set mode to use BOARD numbering
        GPIO.setmode(GPIO.BOARD)

        # designate each pin as input/output and initial values
        GPIO.setup(3, GPIO.OUT)                 # output pin for control of motor via TIP120 base lead (GPIO2)
        # MOVE TO SYNCHRONIZE: GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # input pin for button input, pulled down to provide discrete signal (GPIO14)
        
        try:
            while True:
                print("Motor active for " + duration + " more seconds")
                GPIO.output(3, 1)
                sleep(timeon)                               # keep pin 3 ON for timeon (s)
                GPIO.output(3, 0)
                sleep(timeoff)                              # keep pin 3 OFF for timeoff (s) THIS IS WHEN PICTURE IS TAKEN
                duration = duration - (timeon + timeoff)    # iterate duration downwards by interval (s) until duration is 0
                if duration < (timeon + timeoff):           # if remaining duration is less than timeon + timeoff cycle time, break from loop         
                    break
                
            print("Cycle finished")
            GPIO.output(3, 0)   # turn off motor

        except KeyboardInterrupt:
            print("Stopping motor")
            GPIO.output(3, 0)   # turn off motor
        except:
            print("An exception occurred (motor)")  # if code is unsuccessful return error message
            
        finally:
            GPIO.cleanup()                          # revert settings to prevent damage to GPIO and RPi

    def camera(self):
        
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # input pin for button input, different button with but connected to same 3v3 power pin 1

        try:
            if GPIO.input(12) == 1:
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
        
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # using same input pin as camera button, camera will trigger once every light change (6 times)

        try:
            if GPIO.input(12) == 1:
                print("Input pin 12 is HIGH - trigger lighting change")
                GPIO.output(11, 1)          # set pin 11 output to HIGH/1, trigger light change
            else:
                print("Input pin 12 is LOW - don't trigger lighting change")
                GPIO.output(11, 0)          # set pin 11 output to LOW/0, do not trigger light change

        except:
            print("An exception occurred (light)")

        finally:
            GPIO.cleanup()
            
    
