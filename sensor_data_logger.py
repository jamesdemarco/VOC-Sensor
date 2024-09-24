import serial
import pandas as pd
from datetime import datetime
import os


def log_sensor_data():
    # Change this to your Arduino's serial port
    ser = serial.Serial('/dev/cu.usbmodem14101', 9600)
    data = []
    file_path = '/Users/jamesdemarco/sensor_data.xlsx'

    def save_data(data):
        df = pd.DataFrame(data, columns=['Timestamp', 'BME_Temperature', 'BME_Pressure', 'BME_Humidity',
                                         'BME_Gas_Resistance', 'SHT_Temperature', 'SHT_Humidity', 'GM102B_PPM',
                                         'GM102B_Vol', 'GM302B_PPM', 'GM302B_Vol', 'GM502B_PPM', 'GM502B_Vol',
                                         'GM702B_PPM', 'GM702B_Vol', 'GM_NO2'])

        print(f"Saving data to {file_path}")
        if os.path.exists(file_path):
            # Append data without writing the header
            df.to_excel(file_path, index=False, mode='a', header=False)
        else:
            # Write data with the header for the first time
            df.to_excel(file_path, index=False, header=True)

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received line: {line}")  # Debugging: Print the received line

            values = line.split(',')
            print(f"Split values: {values}")  # Debugging: Print split values

            if len(values) == 13:  # Ensure all sensor values are received
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data.append([timestamp] + values)

                if len(data) >= 5:  # Save every 5 readings
                    print(f"Data ready to save: {data}")  # Debugging: Print data to save
                    save_data(data)
                    data = []
    except KeyboardInterrupt:
        # Save remaining data when script is stopped
        if data:
            print(f"Data to save on interrupt: {data}")  # Debugging: Print data to save on interrupt
            save_data(data)
        ser.close()
