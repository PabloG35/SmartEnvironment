# config.py
import os

DB_USER = os.getenv('DB_USER', 'teamone')
DB_PASSWORD = os.getenv('DB_PASSWORD', '12345')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'smartenvironmentdb')

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SENSOR_READ_INTERVAL = 5
