import keypadCode

import RPi.GPIO as GPIO
import time

""" PINS """
# These GPIO pins are connected to the keypad
# change these according to your connections!
L1 = 12
L2 = 16
L3 = 20
L4 = 21

C1 = 5
C2 = 6
C3 = 13
C4 = 19

""" PIN SETUP """
# Initialize the GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


""" KEYPAD CLASS """
class keypad:
    def __init__(self, p, s, i):
        self.pressed    = p
        self.secretCode = s
        self.input      = i

    def kpCallback(self, channel):                                                      # Channel = the key pressed
        if self.pressed == -1:
            self.pressed = channel

    def setAllLines(self, state):                                                       # Set the state of each row/line
        GPIO.output(L1, state)
        GPIO.output(L2, state)
        GPIO.output(L3, state)
        GPIO.output(L4, state)

    def checkSpecialKeys(self):                                                         # Check special keys such as 'Enter', 'Clr', and 'Input'
        global input
        global numTries
        global correctCode
        correctCode = False
        pressed = False
        numTries = 0

        GPIO.output(L3, GPIO.HIGH)

        if (GPIO.input(C4) == 1):
            print("Input reset!");
            pressed = True

        GPIO.output(L3, GPIO.LOW)
        GPIO.output(L1, GPIO.HIGH)

        if (not pressed and GPIO.input(C4) ):                       # TODO: We must call this function with flags set for when it checks the password and when it checks for time input
            if numTries < 5:
                if self.input == secretCode:
                    correctCode = True
                    print("Code correct!")
                    numTries = 0                                    # Resets number of tries when code is correct
                    # TODO: Unlock a door, turn a light on, etc.
                else:
                    print("Incorrect code!")
                    # TODO: Sound an alarm, send an email, etc.
                    numTries += 1
            else:
                print("Too many tries.... Wait 5 minutes")
                time.sleep(60*5)
            pressed = True

        GPIO.output(L3, GPIO.LOW)

        global setHour
        global setMinute
        global alarmHour
        global alarmMinute
        global pressCount
        MAX_TIME_PRESS  = 2

        if pressed and not correctCode:
            self.input = ""

        elif pressed and setHour:
            if pressCount < MAX_TIME_PRESS:
                self.alarmHour = ""
                pressCount += 1
            else:
                setHour = False

        elif pressed and setMinute:
            if pressCount < MAX_TIME_PRESS:
                self.alarmMinute = ""
                pressCount += 1
            else:
                setMinute = False

        return pressed

    def readLine(self, line, characters):                                                                       # TODO: Fix this code to be conditional and append to input, hour,
        # global input                                                                                          # or minute, depending on which function is called
        # We have to send a pulse on each line to
        # detect button presses
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(C1) == 1):
            print(characters[0])
            self.input += characters[0]
        if(GPIO.input(C2) == 1):
            print(characters[1])
            self.input += characters[1]
        if(GPIO.input(C3) == 1):
            print(characters[2])
            self.input += characters[2]
        if(GPIO.input(C4) == 1):
            print(characters[3])
            self.input += characters[3]
        GPIO.output(line, GPIO.LOW)

    # def startKeypad(self, reading):
    def startKeypad(self):
        if self.pressed != -1:
            self.setAllLines(GPIO.HIGH)
            if not( GPIO.input(self.pressed) ):
                self.pressed = -1
            else:
                time.sleep(0.1)
        else:
            if not( self.checkSpecialKeys() ):
                # call the readLine function for each row of the keypad
                self.readLine(L1, ["1","2","3","A"])
                self.readLine(L2, ["4","5","6","B"])
                self.readLine(L3, ["7","8","9","C"])
                self.readLine(L4, ["*","0","#","D"])
                time.sleep(0.1)
            else:
                time.sleep(0.1)

    def inputPassword(self):
        global unlocked
        global setHour
        while not correctCode:
            self.startKeypad()
        setHour = True
        print("Input your alarm time:")
        self.inputTime()
    
    def inputTime(self):
        global pressCount
        global setHour
        global setMinute
        
        while setHour:
            self.startKeypad()
        pressCount = 0
        #These two flags need to be set in checkSpecialKeys or in inputPassword
        # Fixed it in checkSpecialKeys
        # setHour = False
        # setMinute = True
        while setMinute:
            self.startKeypad()

        print( f'Time is {alarmHour}:{alarmMinute}' )

########################################################################################################################################################################################################

""" FLAGS """
correctCode     = False
unlocked        = False
setHour         = False
setMinute       = False
pressCount      = 0

keypadPressed   = -1
secretCode      = keypadCode.userPass
input           = ''
alarmHour       = ''
alarmMinute     = ''

KP = keypad(keypadPressed, secretCode, input)                                                                       # Create keypad object

########################################################################################################################################################################################################

""" ISRs """
GPIO.add_event_detect(C1, GPIO.RISING, callback = KP.kpCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback = KP.kpCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback = KP.kpCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback = KP.kpCallback)


########################################################################################################################################################################################################

""" TEST CODE """
if __name__ == '__main__':
    correctCode = False
    # reading = True
    try:
        numTries = 0
        # invalidCode = (KP.self.input != secretCode)
        # KP.startKeypad()
        KP.inputPassword()
        hour, minute = KP.setTime()
        # KP.startKeypad(reading)
    except KeyboardInterrupt:
        print("\nApplication stopped!")