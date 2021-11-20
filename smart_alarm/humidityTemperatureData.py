"""
Name: Michael Ly
Date: October 4, 2021
Description:    Function that gets temperature and humidity from a DHT22
                sensor
                
Target:         Raspberry Pi 4

Dependencies:   adafruit_dht
                time
                RPi.GPIO
                board
"""

import database_credentials

import adafruit_dht
import time
import RPi.GPIO as GPIO
import board
import datetime
import mariadb
import sys

ERROR_DELAY = (float)(2.0)
TABLE_NAME = 'humidity_temperature_data'

dht_sensor_port = 26
dht_sensor_type = adafruit_dht.DHT22
dhtDevice = adafruit_dht.DHT22(board.D26, use_pulseio=False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(dht_sensor_port, GPIO.IN)




# Connect to correct Database
try:
	myDB = mariadb.connect(
		host 		= database_credentials.myHost ,
		user 		= database_credentials.myUser ,
		password	= database_credentials.myPassword ,
		database 	= database_credentials.myDatabase
	)
except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")
	sys.exit(1)
	
# Get cursor
myCursor = myDB.cursor()






# Routine to insert temperature records into the dht22_data table
def getTempandHumidity():
    try:
        temperature_c   = dhtDevice.temperature
        temperature_f   = ( (9/5)*temperature_c ) + 32
        humidity        = dhtDevice.humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(f'\n\n============================================================  {error.args[0]}  ============================================================\n\n')
        time.sleep(ERROR_DELAY)
    except Exception as error:
        dhtDevice.exit()
        # Raise error
        time.sleep(ERROR_DELAY)
    return temperature_c, temperature_f, humidity




def showData(timenow, temperature_c, temperature_f, humidity):
    """ Temperature and Humidity Data (DHT22) """

    # data    = {
    #     "time"		    :	timenow,
    #     "temperatureC"	:	temperature_c,
    #     "temperatureF"	:	temperature_f,
    #     "humidity"	    :	humidity
    # }
    
    print("Humidity and Temperature Data in getData function")
    print("============================================================")
    print('Time     :', timenow.strftime("%a, %B %d, %Y %H:%M:%S"))
    print('Temp     : {:.1f} C / {:.1f} F'.format(temperature_c, temperature_f))
    print('Humidity : {:.1f}%\n'.format(humidity))

def sendData(timenow, temperature_c, temperature_f, humidity):
    sql  		= f"INSERT INTO {TABLE_NAME} (time, temperatureC, temperatureF, humidity) VALUES (%s, %s, %s, %s)"
    val			= (timenow, temperature_c, temperature_f, humidity)

    myCursor.execute(sql, val)
    myDB.commit()




#import Adafruit_DHT
#import board

#DHT_SENSOR = Adafruit_DHT.DHT22
#DHT_PIN = 26

#while True:
#    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

#    if humidity is not None and temperature is not None:
#        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
#    else:
#        print("Failed to retrieve data from humidity sensor")



# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

#import time
#import board
#import adafruit_dht

# Initial the dht device, with data pin connected to:
#dhtDevice = adafruit_dht.DHT22(board.D26)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
#dhtDevice = adafruit_dht.DHT22(board.D26, use_pulseio=False)

#while True:
#    try:
#def getTempandHumidity():
        #try:
        # Print the values to the serial port
                #temperature_c = dhtDevice.temperature
                #temperature_f = temperature_c * (9 / 5) + 32
                #humidity = dhtDevice.humidity
        #print(
            #"Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
            #    temperature_f, temperature_c, humidity
            #)
        #)

        #except RuntimeError as error:
        #if (RuntimeError as error):
        # Errors happen fairly often, DHT's are hard to read, just keep going
        #print(error.args[0])
                #time.sleep(2.0)
        #except Exception as error:
        #if (Exception as error):
                #dhtDevice.exit()
         #       raise error

                #time.sleep(2.0)
        
        #return temperature_c, temperature_f, humidity
        
        
        
        
        
        
        
        




