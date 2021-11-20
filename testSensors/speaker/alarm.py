import schedule
import subprocess
import time


""" FLAGS """
ALARM_ON            = (bool)(False)

""" CONSTANTS """
SCHEDULE_DELAY_S    = 1
SLEEP_DELAY         = 1

# .wav file to open with subprocess
alarmFile = 'aplay /home/pi32/Music/emotional-piano-melody_124bpm_A_major.wav'


def job():
    global ALARM_ON
    subprocess.call([alarmFile], shell=True)
    ALARM_ON = True


schedule.every(1).seconds.do(job)                                         # Debug code to check if BT speaker is connected
schedule.every().thursday.at('06:32').do(job)
# schedule.every().day.at('17:05').do(job)                                  # TODO: Make this a function and call it in a thread
# schedule.every().day.at(f'{keypad.hour}:{keypad.minute}').do(job)         # TODO: Receive arguments from the keypad to select WHEN to turn on alarm
                                                                            # TODO: Make a conditional statement in the main program to turn off the alarm
                                                                            #       and then actuate something like an email prompting that you woke up today

while not ALARM_ON:
    schedule.run_pending()
    time.sleep(SLEEP_DELAY)
    pass

while ALARM_ON:
#     try:
#         schedule.run_pending()
#         time.sleep(1)
        try:
            schedule.run_pending()
            time.sleep(SLEEP_DELAY)
            schedule.every(SCHEDULE_DELAY_S).second.do(job)
        except KeyboardInterrupt:
            ALARM_ON = False
