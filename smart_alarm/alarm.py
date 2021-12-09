import distanceData
import emailData
import keypadData as kp   #TODO: rewrite this module with classes(?) because it runs in the background, might have to do more multithreading and then send correct message to startAlarm
import schedule
import subprocess
import time
import smtplib
# from threading import Thread, Lock

""" FLAGS """
ALARM_ON            = (bool)(False)

""" CONSTANTS """
SCHEDULE_DELAY_S    = 2
SLEEP_DELAY         = 3
TURN_OFF_DISTANCE   = (float)(50.0)
ALARM_HR            = '09'
ALARM_MIN           = '30'


# .wav file to open with subprocess
pianoAlarm  = 'aplay /home/pi32/Music/emotional-piano-melody_124bpm_A_major.wav'
schoolAlarm = 'aplay /home/pi32/Music/SchoolBell.wav'

def job():
    global ALARM_ON
    # subprocess.call([pianoAlarm], shell=True)
    subprocess.call([schoolAlarm], shell=True)
    ALARM_ON = True

def startAlarm():
    numSounds = 0

    # schedule.every(3).seconds.do(job)                                             # Debug code to check if BT speaker is connected
    schedule.every().Tuesday.at(f'{ALARM_HR}:{ALARM_MIN}').do(job)                      # TODO: Use keypad to set a new alarm time and require user password
    # schedule.every().thursday.at(f'{kp.hourSet}:{kp.minuteSet}').do(job)

    global ALARM_ON
    # if not ALARM_ON:
    while not ALARM_ON:
        schedule.run_pending()
        time.sleep(SLEEP_DELAY)
        pass
    # if ALARM_ON:
    while ALARM_ON:
        distance = round(float(distanceData.FindDistance()),2)                       # Get Distance
        # time.sleep(0.5)
        try:
            if (distance > TURN_OFF_DISTANCE):
                # print('Alarm is on...\n')
                schedule.run_pending()
                time.sleep(SLEEP_DELAY)
                schedule.every(SCHEDULE_DELAY_S).seconds.do(job)
                numSounds += 1
            else:
                ALARM_ON = False
                time.sleep(1)
                print('Alarm is off...\n')
        except KeyboardInterrupt:
            ALARM_ON = False
            print('exiting...')
    emailData.sendDistanceError(distance, numSounds)

if __name__ == "__main__":
    print(f'Setting alarm for {ALARM_HR}:{ALARM_MIN}')
    startAlarm()