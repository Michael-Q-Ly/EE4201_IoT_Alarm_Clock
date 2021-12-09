import database_credentials

import RPi.GPIO as GPIO
import board
import adafruit_dht
import time
import datetime
import mariadb
import sys

# Settings for database connection
dht_sensor_port = 26
dht_sensor_type = adafruit_dht.DHT22
dhtDevice = adafruit_dht.DHT22(board.D26, use_pulseio=False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(dht_sensor_port, GPIO.IN)
GPIO.setmode(GPIO.BCM)
  
GPIO_TRIGGER = 17
GPIO_ECHO = 27
 
GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

SPEED_OF_SOUND = 34300                                              # The speed of sound in cm/s
TABLE_NAME = 'distance_data'


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


def FindDistance():
    GPIO.output(GPIO_TRIGGER, True)                                 # Send a signal out for 0.1 ms
    time.sleep(0.00001)                                             # and then stop
    GPIO.output(GPIO_TRIGGER, False)
  
    StartTime = time.time()
    StopTime = time.time()
  
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
  
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    TimeElapsed = StopTime - StartTime
    distance    = (TimeElapsed * SPEED_OF_SOUND) / 2                # Speed of sound = 34300 cm/s;
                                                                    # Divide by 2 because echo bounces back
  
    return distance

def showData(timenow, distance):
    """ Distance Data (HC_SR04) """

    # data    = {
    #     "time"		:	timenow,
    #     "distance"	: 	distance
    # }

    print("Distance Data in getData Function")
    print("============================================================")
    print('Time     :', timenow.strftime("%a, %B %d, %Y %H:%M:%S"))
    print('Distance : {:.2f} cm\n'.format(distance) )
    # print(data)


def sendData(timenow, distance):
    sql  		= f'INSERT INTO {TABLE_NAME} (time, distance) VALUES (%s, %s)'
    val			= (timenow, distance)

    myCursor.execute(sql, val)
    myDB.commit()