"""
PIR Sensor Data
"""

from gpiozero import MotionSensor
PORT = 18
pir = MotionSensor(PORT)
j = 0
# def getMotionData():
while True:
    j += 1
    print("No Motion\n")
    print(j)
    pir.wait_for_active
    print("....................................You moved\n")
    pir.wait_for_inactive
	# pirPort.wait_for_motion()
	# print("You moved")
	# pirPort.wait_for_no_motion()