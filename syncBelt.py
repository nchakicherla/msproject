class syncBelt:
    
    def __init__(self, interval):
        self.interval = interval
        
    def motor(self, duration):
        
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
                duration = duration - interval  # iterate duration downwards until it equals 0 (motor operation complete)
                print(duration + " seconds remain")

        except:
            print("An exception occurred")  # if code is unsuccessful return error message
            
        finally:
            GPIO.cleanup()                  # revert settings to prevent damage to GPIO and RPi

    def camera(self):

        # import RPi.GPIO module for using pins
        import RPi.GPIO as GPIO
        from time import sleep

        

        

    
