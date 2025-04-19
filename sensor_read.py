import time
import board
import adafruit_dht

# Sensor Logic
dhtDevice = adafruit_dht.DHT11(board.D4)

if __name__ == '__main__':
    while True:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print(f"Temp: {temperature:.1f}°C   Humidity: {humidity:.1f}%")
        except Exception as error:
            print("Reading again...", error)
        time.sleep(2)
