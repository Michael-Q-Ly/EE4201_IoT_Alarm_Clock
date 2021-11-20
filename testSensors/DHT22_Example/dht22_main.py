import Adafruit_DHT as dht
from time import sleep
 
 
def main():
    try:
        while 1:
            humidity, temp = dht.read_retry(dht.DHT22, 23)
            print(f"Temperature={temp:0.1f}, humidity={humidity:0.1f}")
            sleep(10)
 
    except KeyboardInterrupt:
        pass
 
 
if __name__ == "__main__":
    main()
