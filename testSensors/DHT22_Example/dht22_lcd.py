
import Adafruit_DHT as dht
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
 
 
def create_lcd():
    lcd = Adafruit_CharLCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=21, cols=16, lines=2)
    lcd.create_char(1, [0xc, 0x12, 0x12, 0xc, 0x0, 0x0, 0x0, 0x0])  # degree symbol
    lcd.blink(False)
    return lcd
 
 
def main():
    try:
        lcd = create_lcd()
        while 1:
            humidity, temp = dht.read_retry(dht.DHT22, 23)
            lcd.set_cursor(0, 0)
            lcd.message(f"Temp: {temp:0.1f} \x01C")
            lcd.set_cursor(0, 1)
            lcd.message(f"Humidity: {humidity:0.1f}%")
            print(f"LCD updated with temperature={temp:0.1f}, humidity={humidity:0.1f}")
            sleep(10)
 
    except KeyboardInterrupt:
        lcd.clear()
 
 
if __name__ == "__main__":
    main()
