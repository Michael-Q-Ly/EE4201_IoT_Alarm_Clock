import signal
import sys
import time
import RPi.GPIO as GPIO
BUTTON_GPIO = 25

""" Poll """
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pressed = False
    
    while True:
        # button is pressed when pin is LOW
        if not GPIO.input(BUTTON_GPIO):
            if not pressed:
                print("Button pressed!")
                pressed = True
        # button not pressed (or released)
        else:
            pressed = False
        time.sleep(0.1)

""" ISR add_event_detect """
# def signal_handler(sig, frame):
#     GPIO.cleanup()
#     sys.exit(0)
# def button_pressed_callback(channel):
#     print("Button pressed!")
# if __name__ == '__main__':
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, 
#             callback=button_pressed_callback, bouncetime=100)
    
#     signal.signal(signal.SIGINT, signal_handler)
#     signal.pause()