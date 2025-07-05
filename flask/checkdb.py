import sqlite3 as sql

conn = sql.connect("Sensors.db")
cursor = conn.cursor()

# View contents of each table
print("\nSensortypes:")
for row in cursor.execute("SELECT * FROM Sensortypes"):
    print(row)

print("\nSensors:")
for row in cursor.execute("SELECT * FROM Sensors"):
    print(row)

print("\nMeasurements:")
for row in cursor.execute("SELECT * FROM Measurements"):
    print(row)

conn.close()

