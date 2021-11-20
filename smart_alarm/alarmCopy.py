import distanceData
import emailData
# import keypadData as kp   #TODO: rewrite this module with classes(?) because it runs in the background, might have to do more multithreading and then send correct message to startAlarm
import keypadCode

import schedule
import subprocess
import time
import smtplib
# from threading import Thread, Lock
import RPi.GPIO as GPIO
# from gpiozero import Button

############################################################################################################################################################################
""" PIN SETUP """
# Keypad
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
# Button ISR 


# Setup
keypadPressed = -1
secretCode = keypadCode.userPass
input = ""

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

# INTERRUPTS
BUTTON = 25
# Button is an input pulled up to avoid false detection.
# On button press, GND is connected. We look for falling
# edge
GPIO.setup( BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP )
# Setup
buttonPressed = 0



############################################################################################################################################################################
""" FLAGS """
ALARM_ON            = (bool)(False)
############################################################################################################################################################################
""" CONSTANTS """
SCHEDULE_DELAY_S    = 1
SLEEP_DELAY         = 3
TURN_OFF_DISTANCE       = (float)(50.0)
############################################################################################################################################################################
# .wav file to open with subprocess
pianoAlarm  = 'aplay /home/pi32/Music/emotional-piano-melody_124bpm_A_major.wav'
schoolAlarm = 'aplay /home/pi32/Music/SchoolBell.wav'
# validPassword = (bool)(False)
############################################################################################################################################################################
""" Function Definitions """

def job():
    global ALARM_ON
    # subprocess.call([pianoAlarm], shell=True)
    subprocess.call([schoolAlarm], shell=True)
    ALARM_ON = True


#def startAlarm():
# schedule.every(1).seconds.do(job)                                         # Debug code to check if BT speaker is connected
schedule.every().thursday.at('06:32').do(job)
    # schedule.every().day.at('17:05').do(job)                                  # TODO: Make this a function and call it in a thread
    # schedule.every().day.at(f'{keypad.hour}:{keypad.minute}').do(job)         # TODO: Receive arguments from the keypad to select WHEN to turn on alarm
                                                                                # TODO: Make a conditional statement in the main program to turn off the alarm
                                                                                #       and then actuate something like an email prompting that you woke up today
def startAlarm():
    numSounds = 1

    # schedule.every(3).seconds.do(job)                                         # Debug code to check if BT speaker is connected
    # schedule.every().thursday.at('06:32').do(job)                             # TODO: Use keypad to set a new alarm time and require user password
    # schedule.every().thursday.at('{kp.hourSet}:{kp.minuteSet}').do(job)
    alarmTime = '14'+':'+'55'
    schedule.every().day.at(alarmTime).do(job)
    print(f'Alarm set for {alarmTime}')

    global ALARM_ON
    # if not ALARM_ON:
    while not ALARM_ON:
        schedule.run_pending()
        time.sleep(SLEEP_DELAY)
        pass
    # if ALARM_ON:
    while ALARM_ON:
        # try:
        #     schedule.run_pending()
        #     time.sleep(SLEEP_DELAY)
        #     schedule.every(SCHEDULE_DELAY_S).second.do(job)
        # except KeyboardInterrupt:
        #     ALARM_ON = False
        distance = round(float(distanceData.FindDistance()),2)                       # Get Distance
        # password = kp.input
        try:
            # if (password != kp.secretCode):
            if (distance > TURN_OFF_DISTANCE):
                print('Alarm is on...\n')
                schedule.run_pending()
                time.sleep(SLEEP_DELAY)
                schedule.every(SCHEDULE_DELAY_S).second.do(job)
                numSounds += 1
            else:
                ALARM_ON = False
                time.sleep(3)
                print('Alarm is off...\n')
                # return ALARM_ON
        except KeyboardInterrupt:
            ALARM_ON = False
            print('exiting...')
    emailData.sendDistanceError(distance, numSounds)


if __name__ == '__main__':
    startAlarm()



# """ FLAGS """
# ALARM_ON            = (bool)(False)

# """ CONSTANTS """
# SCHEDULE_DELAY_S    = 1
# SLEEP_DELAY         = 3
# TURN_OFF_DISTANCE       = (float)(50.0)

# # .wav file to open with subprocess
# pianoAlarm  = 'aplay /home/pi32/Music/emotional-piano-melody_124bpm_A_major.wav'
# schoolAlarm = 'aplay /home/pi32/Music/SchoolBell.wav'
# # validPassword = (bool)(False)

# def job():
#     global ALARM_ON
#     # subprocess.call([pianoAlarm], shell=True)
#     subprocess.call([schoolAlarm], shell=True)
#     ALARM_ON = True


# #def startAlarm():
# # schedule.every(1).seconds.do(job)                                         # Debug code to check if BT speaker is connected
# # schedule.every().thursday.at('06:32').do(job)
#     # schedule.every().day.at('17:05').do(job)                                  # TODO: Make this a function and call it in a thread
#     # schedule.every().day.at(f'{keypad.hour}:{keypad.minute}').do(job)         # TODO: Receive arguments from the keypad to select WHEN to turn on alarm
#                                                                                 # TODO: Make a conditional statement in the main program to turn off the alarm
#                                                                                 #       and then actuate something like an email prompting that you woke up today

# # def startAlarm(validPassword):    #TODO: shared memory with a multithread; must use a mutex / lock
# # def startAlarm(distance, stuff):
# def startAlarm():
#     numSounds = 1

#     schedule.every(3).seconds.do(job)                                         # Debug code to check if BT speaker is connected
#     schedule.every().thursday.at('06:32').do(job)                               # TODO: Use keypad to set a new alarm time and require user password
#     # schedule.every().thursday.at('{kp.hourSet}:{kp.minuteSet}').do(job)
#     schedule.every().day.at('14:10').do(job)

#     global ALARM_ON
#     if not ALARM_ON:
#     # while not ALARM_ON:
#         schedule.run_pending()
#         time.sleep(SLEEP_DELAY)
#         pass
#     if ALARM_ON:
#     # while ALARM_ON:
#         # try:
#         #     schedule.run_pending()
#         #     time.sleep(SLEEP_DELAY)
#         #     schedule.every(SCHEDULE_DELAY_S).second.do(job)
#         # except KeyboardInterrupt:
#         #     ALARM_ON = False
#         distance = round(float(distanceData.FindDistance()),2)                       # Get Distance
#         # password = kp.input
#         try:
#             # if (password != kp.secretCode):
#             if (distance > TURN_OFF_DISTANCE):
#                 print('Alarm is on...\n')
#                 schedule.run_pending()
#                 time.sleep(SLEEP_DELAY)
#                 schedule.every(SCHEDULE_DELAY_S).second.do(job)
#                 numSounds += 1
#             else:
#                 ALARM_ON = False
#                 time.sleep(3)
#                 print('Alarm is off...\n')
#                 # return ALARM_ON
#         except KeyboardInterrupt:
#             ALARM_ON = False
#             print('exiting...')
#     emailData.sendDistanceError(distance, numSounds)
        

# # startAlarm()

# # lock = Lock()
# # def getPassword():
# #     global reading
# #     global validPassword
# #     global ALARM_ON

# #     reading         = True
# #     validPassword   = False
# #     while reading:
# #         lock.acquire()
# #         if not validPassword:
# #             validPassword = kp.getKeyPress(reading)
# #         else:
# #             reading     = False
# #             ALARM_ON    = False
# #         lock.release()

# # passwordThread = Thread( target = getPassword, args = () )
# # passwordThread.daemon = True
# # passwordThread.start()


# # alarmThread = Thread( target = startAlarm, args = (ALARM_ON) )
# # alarmThread.daemon = True
# # alarmThread.start()

# # passwordThread.join()
# # alarmThread.join()