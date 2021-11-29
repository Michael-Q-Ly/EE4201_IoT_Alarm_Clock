# import distanceData
import humidityTemperatureData

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time

SENSOR_DELAY = (float)(3.0)
ERROR_DELAY  = (float)(2.0)

lcd = LCD()
def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

# while True:
# def displayLCD():
def displayLCD(temperatureC, temperatureF, humidity):
    # while True:
        # try:
        #     # distance = distanceData.FindDistance()
        #     temperatureC, temperatureF, humidity = humidityTemperatureData.getTempandHumidity()
        # except RuntimeError as error:
        #     # Errors happen fairly often, DHT's are hard to read, just keep going
        #     print(f'\n\n============================================================  {error.args[0]}  ============================================================\n\n')
        #     time.sleep(ERROR_DELAY)
        # except Exception as error:
        #     humidityTemperatureData.dhtDevice.exit()
        #     # Raise error
        #     time.sleep(ERROR_DELAY)
        try:
            # signal(SIGTERM, safe_exit)
            # signal(SIGHUP, safe_exit)
            lcd.text(time.strftime('%I:%M:%S %p'), 1)
            lcd.text(time.strftime('%a %b %d, 20%y'), 2)
            print('....................................................................................................................................Time is showing\n')
            # pause()
            time.sleep(SENSOR_DELAY)
            lcd.text('{:.1f}C  /  {:.1f}F'.format(temperatureC, temperatureF), 1)
            lcd.text('{:.1f}% humidity'.format(humidity), 2)
            # pause()
            print('............................................................................................................Data is showing\n')

            
            """ Temperature and Humidity Data (DHT22) """
            print('                                 Humidity and Temperature Data in LCD')
            print('                                 ============================================================')
            print('                                 Temp     : {:.1f} C / {:.1f} F'.format(temperatureC, temperatureF))
            print('                                 Humidity : {:.1f}%\n'.format(humidity))

            
            time.sleep(SENSOR_DELAY)
            print('displayLCD thread closed\n\n')
        except KeyboardInterrupt:
            pass
        finally:
            lcd.clear()
            time.sleep(0.1)


if __name__ == "__main__":
    displayLCD()