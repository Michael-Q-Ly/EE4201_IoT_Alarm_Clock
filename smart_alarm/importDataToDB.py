# import database_credentials
import displayData
import distanceData
import emailData
import humidityTemperatureData
import alarm
# import motionData

# import mariadb
import datetime
import time
# import sys
# import smtplib
from signal import signal, SIGTERM, SIGHUP, pause
# from rpi_lcd import LCD
from threading import Thread, Lock
import subprocess
# import schedule
####################################################################################################################################################################################################

""" CONSTANTS """

SENSOR_DELAY            = (float)(2.0)
ERROR_DELAY             = (float)(0.5)
SECONDS_TO_MINUTES      = (float)(60.0)
MINUTES_TO_HOURS        = (float)(60.0)
NUM_HOURS               = (float)(1.0)
SEND_TO_CLOUD_DELAY_HR   = (float)( SECONDS_TO_MINUTES * MINUTES_TO_HOURS * NUM_HOURS )
# SEND_TO_CLOUD_DELAY_HR  = (float)(5.0)                                                                                # DEBUG - Delay only 5 seconds to see output is working properly
TIME_COUNTER_DELAY      = (float)(1.00)

####################################################################################################################################################################################################

""" FLAGS """

PRINT_TO_CONSOLE        = (bool)(True)
ALARM_ON                = (bool)(True)
USE_LCD                 = (bool)(True)
USE_CLOUD               = (bool)(False)
####################################################################################################################################################################################################

lock = Lock()   # Mutex to make sure data is retrieved before outputting to LCD screen

"""
Counter function counts seconds the program has been active
"""
def counter():
    global count
    count = 0 ;
    while True:
        print(f'                                                                        {count}                                                                        ')
        time.sleep(TIME_COUNTER_DELAY)
        count += 1
####################################################################################################################################################################################################
"""
getData function gets the current time, distance, temperature, and humidity
sensor readings and does exception handling for bad reads
It then shows the data
"""
def getData():
    global timenow
    global distance
    global temperature_c
    global temperature_f
    global humidity

    print('Getting sensor data...\n')
    """ Data Collection """
    validData = (bool)(False)
    lock.acquire()
    # while not validData and errorCount < 5:
    while not validData:
        try:
            timenow                                 = datetime.datetime.now()                                           # Get Time
            # distance                                = round(float(distanceData.FindDistance()),2)                     # Get Distance
            temperature_c, temperature_f, humidity  = humidityTemperatureData.getTempandHumidity()                      # Get Temperature in C and F, and humidity
            validData = True
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(f'\n\n============================================================  {error.args[0]}  ============================================================\n\n')
            validData = False
            time.sleep(ERROR_DELAY)
        except Exception as error:
            validData = False
            humidityTemperatureData.dhtDevice.exit()
            # Raise error
            time.sleep(ERROR_DELAY)
        finally:
            lock.release()                                                                                              # Release data retrieval mutex

    if PRINT_TO_CONSOLE:
        # distanceData.showData(timenow, distance)
        humidityTemperatureData.showData(timenow, temperature_c, temperature_f, humidity)
    
    
    print('getData thread closed\n\n')

    """ If you want to send data to the cloud from here.... """
        # print('Sending data...\n')
        # distanceData.sendData(timenow, distance)
        # humidityTemperatureData.sendData(timenow, temperature_c, temperature_f, humidity)
        # time.sleep(SEND_2_CLOUD_DELAY_HR)

        # return timenow, distance, temperature_c, temperature_f, humidity
####################################################################################################################################################################################################
"""
Send telemetry data to the cloud to process
"""
def sendData(timenow, distance, temperature_c, temperature_f, humidity):
    """ Display sent data"""
    print('Sending data...\n')
    # distanceData.sendData(timenow, distance)
    humidityTemperatureData.sendData(timenow, temperature_c, temperature_f, humidity)
    # Send the data to the cloud after specified hours or fraction of hours
    time.sleep(SEND_TO_CLOUD_DELAY_HR)
####################################################################################################################################################################################################

""" Counter """
counterThread = Thread( target = counter, args = () )
counterThread.daemon = True
counterThread.start()

""" Get data from sensors after a delay and rectify any bad reads """
while True:
    """ Data """
    getDataThread = Thread( target = getData, args = () )
    getDataThread.daemon = True
    getDataThread.start()
    getDataThread.join()
    
    """ LCD """
    if USE_LCD:
        print('Using 1602 LCD\n')
        displayThread = Thread( target = displayData.displayLCD, args = (temperature_c, temperature_f, humidity) )
        displayThread.daemon = True
        displayThread.start()
    else:
        print('LCD is OFF\n')


    """ Send to CloudSQL """
    if USE_CLOUD:
        print('Porting data to the cloud...\n')
        dataThread = Thread( target = sendData, args = (timenow, temperature_c, temperature_f, humidity) )
        # dataThread = Thread( target = sendData, args = (timenow, distance, temperature_c, temperature_f, humidity) )
        dataThread.daemon = True
        dataThread.start()
    else:
        print('Not sending data to cloud\n')


    """ Alarm On """
    if ALARM_ON:
        print('Alarm is ON\n')
        alarmThread = Thread( target = alarm.startAlarm, args = () )
        alarmThread.daemon = True
        alarmThread.start()
    else:
        print('Alarm is currently OFF')
    
    
    if USE_LCD:
        displayThread.join()
    if ALARM_ON:
        alarmThread.join()
    print('====================================================================================================================================================')