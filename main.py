"""
This is a program to provide a UI for Temperature, Pressure, Humidity, and Gas sensors.
Sensors used are the Adafruit BME680, Adafruit SHT45, and Grove Multichannel Gas Sensor.
They report to an ELEGOO Uno R3, running Arduino IDE program SensorTest

Written by James DeMarco for Raven Space Systems, 2024
"""

from UI.sensor_readings_app import SensorReadingsApp
import customtkinter as ctk
import threading
from Data_Logging.sensor_data_logger import log_sensor_data

if __name__ == "__main__":
    # Start the data logging in a separate thread
    logging_thread = threading.Thread(target=log_sensor_data)
    logging_thread.daemon = True  # Allow the thread to exit when the main program exits
    logging_thread.start()

    #root = ctk.CTk()
    #app = SensorReadingsApp(root)
    #root.protocol("WM_DELETE_WINDOW", app.on_closing)
    #root.mainloop()

try:
    while True:
        pass  # Keep the script running
except KeyboardInterrupt:
    print("Terminated and cleaned up.")
