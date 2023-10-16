import serial

# Open a serial connection to your Arduino
ser = serial.Serial('COM7', 9600)  # Adjust 'COM7' to match your Arduino's serial port

# Open a text file for writing
with open('rfid_tags.txt', 'a') as file:
    while True:
        data = ser.readline().strip()
        if data:
            print("Received data:", data)
            file.write(data.decode() + '\n')
            file.flush()  # Flush the data to the file
            
    file.close()  # Close the file