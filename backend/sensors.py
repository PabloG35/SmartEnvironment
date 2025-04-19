import time
import board
import adafruit_dht

# Initialize the DHT11 sensor on pin D4
dht_device = adafruit_dht.DHT11(board.D4)

def get_temperature(retries=5, delay=2):
    """
    Attempts to read the temperature (°C) from the DHT11 sensor up to 'retries' times.
    Waits 'delay' seconds between attempts.
    Returns the temperature if successful, otherwise returns None.
    """
    for attempt in range(retries):
        try:
            temperature = dht_device.temperature
            if temperature is not None:
                return temperature
        except Exception as error:
            print(f"Error reading temperature (attempt {attempt+1}/{retries}): {error}")
        time.sleep(delay)
    return None

def get_humidity(retries=5, delay=2):
    """
    Attempts to read the humidity (%) from the DHT11 sensor up to 'retries' times.
    Waits 'delay' seconds between attempts.
    Returns the humidity if successful, otherwise returns None.
    """
    for attempt in range(retries):
        try:
            humidity = dht_device.humidity
            if humidity is not None:
                return humidity
        except Exception as error:
            print(f"Error reading humidity (attempt {attempt+1}/{retries}): {error}")
        time.sleep(delay)
    return None

if __name__ == "__main__":
    # Test the sensor readings in standalone mode
    while True:
        temperature = get_temperature()
        humidity = get_humidity()
        if temperature is not None and humidity is not None:
            print(f"Temp: {temperature:.1f}°C   Humidity: {humidity:.1f}%")
        else:
            print("Error reading sensor, trying again...")
        time.sleep(2)
