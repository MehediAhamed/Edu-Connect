import serial
import sqlite3
import sys

port = 'COM7'

try:
    ser = serial.Serial(port, 9600)
except serial.SerialException:
    print(f"Failed to open serial port {port}. Please make sure it's connected.")
    sys.exit(1)

# Connect to the SQLite database (create or open the database file)
conn = sqlite3.connect('new.db')  # This will create a SQLite database file if it doesn't exist

# Create a cursor to interact with the database
cursor = conn.cursor()

# Create a table to store RFID tag data if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  tag TEXT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# Save changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()

try:
    while ser.is_open:  # Check if the serial port is open
        data = ser.readline().strip()
        if data:
            print("Received data:", data)

            conn = sqlite3.connect('new.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO attendance (tag) VALUES (?)", (data.decode(),))
            conn.commit()
            cursor.close()
            conn.close()
except KeyboardInterrupt:
    print("Program stopped by user.")
except serial.SerialException:
    print(f"Serial port {port} was disconnected. Program terminated.")
finally:
    ser.close() 
