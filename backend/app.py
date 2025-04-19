#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
from sensors import get_temperature
from models import SessionLocal, SensorReading, init_db  # SQL code now enabled
from config import SENSOR_READ_INTERVAL
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize the database (create tables if they don't exist)
init_db()

# Global variable for the latest valid temperature
current_temperature = None

def sensor_loop():
    global current_temperature
    while True:
        temperature = get_temperature()
        if temperature is not None:
            current_temperature = temperature
            # Insert the new reading into the database with a timestamp.
            db = SessionLocal()
            try:
                # Check if there are already 10 records.
                count = db.query(SensorReading).count()
                if count >= 10:
                    # Find the oldest reading and delete it.
                    oldest = db.query(SensorReading).order_by(SensorReading.timestamp.asc()).first()
                    if oldest:
                        db.delete(oldest)
                        db.commit()  # Commit deletion before inserting new one.
                # Create a new SensorReading and insert it.
                reading = SensorReading(temperature=temperature, timestamp=datetime.utcnow())
                db.add(reading)
                db.commit()
                print(f"[{datetime.utcnow()}] Stored temperature: {temperature}°C in SQL")
            except Exception as e:
                print("Error storing temperature in DB:", e)
                db.rollback()
            finally:
                db.close()
        else:
            print("Error reading temperature.")
        time.sleep(SENSOR_READ_INTERVAL)

@app.route('/sensor_data', methods=['GET'])
def sensor_data():
    """
    Returns a dummy message since SQL storage is now enabled.
    (You can update this endpoint later as needed.)
    """
    return jsonify({"message": "SQL storage is enabled."})

@app.route('/live_temperature', methods=['GET'])
def live_temperature():
    """
    Returns the latest temperature reading from the database.
    """
    db = SessionLocal()
    try:
        # Query for the most recent reading by timestamp.
        reading = db.query(SensorReading).order_by(SensorReading.timestamp.desc()).first()
        if reading:
            return jsonify({
                "temperature": reading.temperature,
                "timestamp": reading.timestamp.isoformat()
            }), 200
        else:
            return jsonify({"error": "No temperature reading available in DB."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

if __name__ == "__main__":
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
