import RPi.GPIO as GPIO
import time
  
GPIO.setmode(GPIO.BCM)
  
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
  
def FindDistance():
    GPIO.output(GPIO_TRIGGER, True)
  
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
  
    StartTime = time.time()
    StopTime = time.time()
  
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
  
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
  
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2  # Speed of sound = 34300 m/s
                                          # Divide by 2 because echo bounces back
  
    return distance
