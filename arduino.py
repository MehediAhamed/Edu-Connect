# import serial
# import sqlite3
# import time
# from datetime import datetime

# port = 'COM7'

# while True:
#     try:
#         ser = serial.Serial(port, 9600)
#         print(f"Connected to {port}")
#         break  # Exit the loop if the connection is successful
#     except serial.SerialException:
#         print(f"Waiting for connection...")
#         time.sleep(3)  # Wait for 3 seconds before trying again

# try:
#     while ser.is_open:
#         data = ser.readline().strip()
#         if data:
#             print("Received data:", data)
#             if data.decode()!='Error: Buffer overflow detected!':
#                 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Generate a timestamp
#                 conn = sqlite3.connect('db.sqlite3')
#                 cursor = conn.cursor()
#                 cursor.execute("INSERT INTO classroom_attendance (roll_no, timestamp) VALUES (?, ?)", (data.decode(), timestamp))
#                 conn.commit()
#                 cursor.close()
#                 conn.close()
# except KeyboardInterrupt:
#     print("Program stopped by user.")
# except serial.SerialException:
#     print(f"Serial port {port} was disconnected. Waiting for reconnection...")
# finally:
#     ser.close()
