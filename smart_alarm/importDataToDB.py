# import database_credentials
import distanceData
import humidityTemperatureData
# import motionData
import emailTest
import displayData

# import mariadb
import datetime
import time
# import sys
# import smtplib
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from threading import Thread, Lock
# import concurrent.futures
####################################################################################################################################################################################################

""" CONSTANTS """
TURN_OFF_DISTANCE       = (float)(20.0)
SENSOR_DELAY            = (float)(2.0)
ERROR_DELAY             = (float)(0.5)
SECONDS_TO_MINUTES      = (float)(60.0)
MINUTES_TO_HOURS        = (float)(60.0)
NUM_HOURS               = (float)(1.0)
SEND_2_CLOUD_DELAY_HR   = (float)( SECONDS_TO_MINUTES * MINUTES_TO_HOURS * NUM_HOURS )
# SEND_2_CLOUD_DELAY_HR   = (float)(5.0)  # DEBUG - Delay only 5 seconds to see output is working properly
####################################################################################################################################################################################################

""" FLAGS """
INCORRECT_READ          = (bool)(False) # TODO: Exception handling. If incorrect read, set this flag to true, and set it to false for every good read
ALARM_ON                = (bool)(False)
USE_LCD                 = (bool)(True)
USE_CLOUD               = (bool)(False)
####################################################################################################################################################################################################

def getData():
    """ Data Collection """
    timenow                                 = datetime.datetime.now()                                           # Get Time
    distance                                = round(float(distanceData.FindDistance()),2)                       # Get Distance
    temperature_c, temperature_f, humidity  = humidityTemperatureData.getTempandHumidity()                      # Get Temperature in C and F, and humidity

    """ Distance Data (HC_SR04) """
    print("Distance Data")
    print("============================================================")
    print('Time     :', timenow.strftime("%a, %B %d, %Y %H:%M:%S"))
    print('Distance : {:.2f} cm\n'.format(distance) )

    """ Temperature and Humidity Data (DHT22) """
    print("Humidity and Temperature Data")
    print("============================================================")
    print('Time     :', timenow.strftime("%a, %B %d, %Y %H:%M:%S"))
    print('Temp     : {:.1f} C / {:.1f} F'.format(temperature_c, temperature_f))
    print('Humidity : {:.1f}%\n'.format(humidity))

    return timenow, distance, temperature_c, temperature_f, humidity
####################################################################################################################################################################################################

def checkAlarm(distance, ALARM_ON):                                                                             # TODO: Receive data from sensors as argument
    while ALARM_ON:
        if (distance < TURN_OFF_DISTANCE):
            emailTest.sendDistanceError(distance)
            ALARM_ON = False
    while not ALARM_ON:                                                                                         # TODO: Poll for when the alarm is turned on in the future
        pass
####################################################################################################################################################################################################

def sendData(timenow, distance, temperature_c, temperature_f, humidity):
    while True:
        """ Display sent data"""
        distanceData.showData(timenow, distance)
        humidityTemperatureData.showData(timenow, temperature_c, temperature_f, humidity)

        # Send the data to the cloud after specified hours or fraction of hours
        time.sleep(SEND_2_CLOUD_DELAY_HR)
####################################################################################################################################################################################################

""" Get initial data points """ 
try:
    # global timenow
    # global distance
    # global temperature_c
    # global temperature_f
    # global humidity
    timenow, distance, temperature_c, temperature_f, humidity = getData()
except RuntimeError as error:
    # Errors happen fairly often, DHT's are hard to read, just keep going
    print(f'\n\n============================================================  {error.args[0]}  ============================================================\n\n')
    time.sleep(ERROR_DELAY)
except Exception as error:
    # Raise error
    humidityTemperatureData.dhtDevice.exit()
    time.sleep(ERROR_DELAY)
####################################################################################################################################################################################################

""" LCD """
if USE_LCD:
    print('Using 1602 LCD\n')
    displayThread = Thread( target = displayData.displayLCD, args = () )
    # displayThread = Thread( target = displayData.displayLCD, args = (temperature_c, temperature_f, humidity) )
    displayThread.daemon = True
    displayThread.start()
else:
    print('LCD is OFF\n')


""" Send to CloudSQL """
if USE_CLOUD:
    print('Porting data to the cloud...\n')
    dataThread = Thread( target = sendData, args = (timenow, distance, temperature_c, temperature_f, humidity) )
    dataThread.daemon = True
    dataThread.start()
else:
    print('Not sending data to cloud\n')

""" Alarm On """
if ALARM_ON:  # TODO: Put a flag in the main while loop to check for when this is turned off and stop the thread
    print('Alarm is on!\n')
    AlarmThread = Thread( target = checkAlarm, args = (distance) )
    AlarmThread.daemon = True
    AlarmThread.start()
else:
    print('Alarm is currently OFF')

print('====================================================================================================================================================')
####################################################################################################################################################################################################

""" Get data from sensors after a delay and rectify any bad reads """
j=0     #counts seconds
while True:
    print(f'                                                                        {j}                                                                        ')
    j += 1
    time.sleep(SENSOR_DELAY)
    print('Getting Data\n')
    try:
        timenow, distance, temperature_c, temperature_f, humidity = getData()
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(f'\n\n============================================================  {error.args[0]}  ============================================================\n\n')
        time.sleep(ERROR_DELAY)
    except Exception as error:
        humidityTemperatureData.dhtDevice.exit()
        # Raise error
        time.sleep(ERROR_DELAY)
    print('........................Data received!\n')