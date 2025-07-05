from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3 as sql 
import time
from flask import send_file
import os
from flask import Flask, request, jsonify, render_template, render_template_string
app = Flask(__name__)
meta_data = {'id': [], 'timestamp': [], 'value': [], 'type': []}

# SQL table schemas

Sensortypes = """CREATE TABLE IF NOT EXISTS Sensortypes (
    sensor_type TEXT PRIMARY KEY,
    unit TEXT
)""" 

Sensors = """CREATE TABLE IF NOT EXISTS Sensors (
    sensor_id INTEGER PRIMARY KEY,
    Sensor_latitude TEXT,
    Sensor_longitude TEXT,
    Sensor_type TEXT,
    unit TEXT
)"""

Measurements = """CREATE TABLE IF NOT EXISTS Measurements (
    measurement_id INTEGER PRIMARY KEY,
    sensor_id INTEGER,
    timestamp TEXT,
    value REAL,
    FOREIGN KEY (sensor_id) REFERENCES Sensors(sensor_id)
)"""

# Database setup
def setup_database():
    conn = sql.connect("Sensors.db")
    conn.execute("DROP TABLE IF EXISTS Measurements;")
    conn.execute("DROP TABLE IF EXISTS Sensors;")
    conn.execute("DROP TABLE IF EXISTS Sensortypes;")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute(Sensors)
    conn.execute(Sensortypes)
    conn.execute(Measurements)
    conn.commit()
    conn.close()



# Insert into sensor_type
def insert_into_sensor_type(sensortype, unit):
    conn = sql.connect("Sensors.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO Sensortypes (sensor_type, unit)
    VALUES (?, ?)
''', (sensortype, unit))
    conn.commit()
    conn.close()

# Insert into sensor
def insert_into_sensor(Sensor_location, Sensor_type, unit):
    conn = sql.connect("Sensors.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Sensors (Sensor_location, Sensor_type, unit)
    VALUES (?, ?, ?)
''', (Sensor_location, Sensor_type, unit))
    sensor_id = cursor.lastrowid  # This gets the new sensor's ID
    conn.commit()
    conn.close()



# Insert into Measurements
def insert_into_measurement(sensor_id, sensor_value, timestamp):
    conn = sql.connect("Sensors.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Measurements (sensor_id, timestamp, value)
        VALUES (?, ?, ?)
    ''', (sensor_id, timestamp, sensor_value))
    conn.commit()
    conn.close()




# Flask route to store data
@app.route('/store', methods=['POST'])		
def store_data():
	data = request.get_json()
	timestamp = data.get("timestamp", datetime.now().isoformat())
	sensor_value = data.get("sensor_value")
	sensor_type = data.get("sensor_type")
	sensor_id = data.get("sensor_id")
	meta_data['timestamp'].append(timestamp)
	meta_data['value'].append(sensor_value) 
	meta_data['type'].append(sensor_type)
	meta_data['id'].append(sensor_id)
	insert_into_measurement(sensor_id, sensor_value, timestamp)
	return f"Sensor {sensor_type} stored value {sensor_value} at time {timestamp}"

@app.route('/register_sensor', methods=['POST'])	
def register_sensor():
    data = request.get_json()
    location = data.get("location")
    latitude = location[0]
    longitude = location[1]
    sensor_type = data.get("sensor_type")
    unit = data.get("unit")
    conn = sql.connect("Sensors.db", timeout = 1)
    cursor = conn.cursor()
    # Ensure the sensor type exists
    cursor.execute('''
        INSERT OR IGNORE INTO Sensortypes (sensor_type, unit)
        VALUES (?, ?)
    ''', (sensor_type, unit))
    # Check if sensor already exists
    cursor.execute('''
        SELECT sensor_id FROM Sensors 
        WHERE Sensor_latitude = ? AND Sensor_longitude = ? AND Sensor_type = ?
    ''', (latitude,longitude, sensor_type))
    row = cursor.fetchone()
    if row:
        sensor_id = row[0]
    else:
        cursor.execute('''
            INSERT INTO Sensors (Sensor_latitude, Sensor_longitude, Sensor_type, unit)
            VALUES (?,?, ?, ?)
        ''', (latitude, longitude, sensor_type, unit))
        sensor_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"message": "Sensor ensured", "sensor_id": sensor_id})


###web application flask 
@app.route('/fetch', methods=['GET'])

def fetch_data():
    sensor_type = request.args.get("type")
    if not sensor_type:
        return "Missing sensor type", 400

    conn = sql.connect("Sensors.db")
    cursor = conn.cursor()

    query = """
    SELECT m.timestamp, m.value, s.unit
    FROM Measurements m
    JOIN Sensors s ON m.sensor_id = s.sensor_id
    WHERE s.Sensor_type = ?
    ORDER BY m.timestamp ASC
    """
    cursor.execute(query, (sensor_type,))
    rows = cursor.fetchall()
    conn.close()

    # Format as plain text content.
    # Using the sensor type to create a header for the file.
    header_unit = rows[0][2] if rows else ''
    output = f"{sensor_type}\nTimestamp (UTC)\t{header_unit}\n"
    for ts, val, _ in rows:
        output += f"{ts}\t{val}\n"

    # Define the file path for saving the file on the server.
    directory = "/home/oscar/Skrivbord/Final_project/data"
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it does not exist

    file_name = f"{sensor_type}_data.txt"
    file_path = os.path.join(directory, file_name)

    try:
        # Write the output to the file.
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(output)
    except IOError as e:
        return f"Failed to write file: {e}", 500

    # Optionally send the file to the client as a downloadable file.
    # If you don't want to send the file, you can simply return a success message.
    return send_file(file_path, as_attachment=True,
                 download_name=file_name,
                 mimetype='text/plain')




###problem ALWAYS
@app.route('/retrieve', methods=['GET'])
def retrieve_data():
    sensor_id = request.args.get("sensor_id")
    start_time_str = request.args.get("start_time")
    end_time_str = request.args.get("end_time")

    # Validate required parameters
    if not sensor_id or not start_time_str or not end_time_str:
        return "Missing required parameters", 400

    conn = sql.connect("Sensors.db")
    cursor = conn.cursor()

    query = """
    SELECT m.timestamp, m.value, s.Sensor_type, s.unit
    FROM Measurements m
    JOIN Sensors s ON m.sensor_id = s.sensor_id
    WHERE m.sensor_id = ? AND m.timestamp BETWEEN ? AND ?
    ORDER BY s.Sensor_type, m.timestamp ASC
    """
    cursor.execute(query, (sensor_id, start_time_str, end_time_str))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No data found for the specified parameters.", 404

    # Group the rows by sensor type
    grouped = {}
    for ts, val, typ, unit in rows:
        if typ not in grouped:
            grouped[typ] = {"unit": unit, "data": []}
        grouped[typ]["data"].append((ts, val))

    # Use an external template to render the HTML (make sure you have "retrieve.html" in your templates folder)
    return render_template("retrieve.html", grouped=grouped)


@app.route('/')
def index():
    return 'API is running. Try /store or /retrieve or /fetch'





'''
#(only for preview)
@app.route('/view')
def view_data():
    if not meta_data['id']:
        return "No sensor data available."
    
    result = "<h2>Stored Data</h2><ul>"
    for i in range(len(meta_data['id'])):
        result += f"<li>Sensor: {meta_data['id'][i]} with value: {meta_data['value'][i]} at time: {meta_data['timestamp'][i]}</li>"
    result += "</ul>"
    return result
'''    

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=8080)


