import datetime
import sensordata
import time
import mysql.connector

myDB = mysql.connector.connect(
	host 		= "localhost",
	user 		= "group5" ,
	password	= "SmartAlarm3mb3d!" ,
	database 	= "HC_SR04"
)

myCursor = myDB.cursor()

# Loop forever
while True:
    time.sleep(3)
    distance	= round(float(sensordata.FindDistance()),2)
    # timenow		= float( time.time() )
    timenow = datetime.datetime.now()
    data 		= {"time":timenow, "distance" : distance}
    sql  		= "INSERT INTO SENSOR_DATA (time, distance) VALUES (%s, %s)"
    val			= (timenow, distance)
    myCursor.execute(sql, val)
    
    myDB.commit()
    
    print(myCursor.rowcount, "record inserted")
    print(data)
    
    time.sleep(5)
