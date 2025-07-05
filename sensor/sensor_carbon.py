import sqlite3 as sql 
import sys 
import urllib.request
import random
import time
import requests
from datetime import datetime

URL = "http://flask_api:8080/store"
create_URL = "http://flask_api:8080/register_sensor"
def carbon_sensor():
	
	sensor_type = "Carbon"
	sensor_id = sensor_setup(sensor_type)
	while True:
		#measures temprature *Obviously*
		air_quality_value = round(random.uniform(20.0, 30.0), 2)
		timestamp = datetime.now().isoformat(timespec='seconds')
		
		data = {
		"sensor_id": sensor_id,
		"sensor_type": sensor_type, 
		"timestamp": timestamp,
		"sensor_value": air_quality_value 
		}
		try: 
			response = requests.post(URL, json=data)
			print(f"sent: {data}")
		except Exception as e:
			print("failed to send data", e)	
		time.sleep(7)	
		
		
#runs once in air_quality_sensor for setup		
def sensor_setup(sensor_type):
	offset = 0.0005
	location = [59.2 + random.uniform(-(offset), offset), 18.2 + random.uniform(-(offset), offset)]
	unit = "CO2"
	setup_data = {
		"location": location,
		"sensor_type": sensor_type, 
		"unit": unit
		}
	try: 
		response = requests.post(create_URL, json=setup_data)
		response.raise_for_status()
		response_data = response.json()
		print(f"Sensor registered: {response_data}")
		return response_data["sensor_id"]
	except Exception as e:
		print("Failed to register sensor:", e)
		return None
		
if __name__ == '__main__':
	carbon_sensor()
