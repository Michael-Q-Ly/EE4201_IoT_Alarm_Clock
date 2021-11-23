from dht22_iot_manager import IoTManager
import Adafruit_DHT as dht
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
 
READING_INTERVAL_SEC = 900  # 15 mins
 
IOT_STATUS_TO_LCD_SYMBOL = {"offline": "\x01", "online": "\x02", "connecting": "\x03"}
 
 
def create_lcd():
    lcd = Adafruit_CharLCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=21, cols=16, lines=2)
 
    # CharLCD symbols designed at https://www.quinapalus.com/hd44780udg.html
    lcd.create_char(1, [0x0, 0x0, 0xa, 0x0, 0xe, 0x11, 0x0, 0x0])  # sad
    lcd.create_char(2, [0x0, 0x1, 0x3, 0x16, 0x1c, 0x8, 0x0, 0x0])  # checkmark
    lcd.create_char(3, [0x1f, 0x11, 0xa, 0x4, 0xa, 0x11, 0x1f, 0x0])  # hourglass
    lcd.create_char(4, [0xc, 0x12, 0x12, 0xc, 0x0, 0x0, 0x0, 0x0])  # degree symbol
 
    lcd.blink(False)
 
    return lcd
 
 
def lcd_show_iot_sync_status(lcd, status):
    """
    Display IoT sync status in the upper right corner of the LCD
    """
    if status in IOT_STATUS_TO_LCD_SYMBOL:
        lcd.set_cursor(15, 0)
        lcd.message(IOT_STATUS_TO_LCD_SYMBOL[status])
 
 
def main():
    try:
        iot = IoTManager()
        lcd = create_lcd()
 
        while 1:
            lcd.set_cursor(0, 0)
            humi, temp = dht.read_retry(dht.DHT22, 23)
            lcd.message(f"Temp: {temp:0.1f} \x04C")
            lcd.set_cursor(0, 1)
            lcd.message(f"Humidity: {humi:0.1f}%")
            # show hourglass on the LCD while sending data into the cloud
            lcd_show_iot_sync_status(lcd, "connecting")
            res = iot.publish_data(f"{temp:0.1f}", f"{humi:0.1f}")
            # show success or error symbol on the LCD
            lcd_show_iot_sync_status(lcd, "online" if res else "offline")
            sleep(READING_INTERVAL_SEC)
 
    except KeyboardInterrupt:
        pass
 
    # cleanup
    iot.disconnect()
    lcd.clear()
 
 
if __name__ == "__main__":
    main()
    main()
