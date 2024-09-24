# import time
# import threading
import customtkinter as ctk
# from tkinter import messagebox
from Utilities.serial_reader import SerialReader
# from Sensors.BME680 import BME680sensor


class SensorReadingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Sensor Readings')
        self.root.geometry("675x400")

        # initialize application
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        self.create_widgets()

        # initialize serial reader in a new thread
        self.serial_reader = SerialReader(self.update_labels)
        self.serial_reader.start()

    def create_widgets(self):
        self.bme_frame()
        self.sht_frame()
        self.grove_frame()

    def bme_frame(self):
        frame = ctk.CTkFrame(self.root, fg_color="gray30")
        frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        title_label = ctk.CTkLabel(frame, text="BME680", fg_color="gray50", corner_radius=6)
        title_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.bme_temp_label = ctk.CTkLabel(frame, text="Temperature: ")
        self.bme_temp_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.bme_pressure_label = ctk.CTkLabel(frame, text="Pressure: ")
        self.bme_pressure_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

        self.bme_humidity_label = ctk.CTkLabel(frame, text="Humidity: ")
        self.bme_humidity_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        self.bme_gas_label = ctk.CTkLabel(frame, text="Gas: ")
        self.bme_gas_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")

    def sht_frame(self):
        frame = ctk.CTkFrame(self.root, fg_color="gray30")
        frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsw")

        title_label = ctk.CTkLabel(frame, text="SHT45", fg_color="gray50", corner_radius=6)
        title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.sht_temp_label = ctk.CTkLabel(frame, text="Temperature: ")
        self.sht_temp_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.sht_humidity_label = ctk.CTkLabel(frame, text="Humidity: ")
        self.sht_humidity_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

    def grove_frame(self):
        frame = ctk.CTkFrame(self.root, fg_color="gray30")
        frame.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="nsw")

        title_label = ctk.CTkLabel(frame, text="Grove", fg_color="gray50", corner_radius=6)
        title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.grove_label_1 = ctk.CTkLabel(frame, text="Nitrogen Dioxide: ")
        self.grove_label_1.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.grove_label_2 = ctk.CTkLabel(frame, text="Alcohol Gas: ")
        self.grove_label_2.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

        self.grove_label_3 = ctk.CTkLabel(frame, text="VOC: ")
        self.grove_label_3.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        self.grove_label_4 = ctk.CTkLabel(frame, text="Carbon Monoxide: ")
        self.grove_label_4.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")

    def handle_serial_data(self, data):
        self.root.after(0, self.update_labels, data)

    def update_labels(self, serial_input):
        print(serial_input)
        if serial_input.startswith("BME680"):
            bme_readings = serial_input.split(":")[1].split(",")
            self.bme_temp_label.configure(text=f"Temperature: {bme_readings[0]} C")
            self.bme_humidity_label.configure(text=f"Humidity: {bme_readings[2]} %")
            self.bme_pressure_label.configure(text=f"Pressure: {bme_readings[1]} hPa")
            self.bme_gas_label.configure(text=f"Gas Resistance: {bme_readings[3]} ohms")
        elif serial_input.startswith("SHT4x"):
            sht_readings = serial_input.split(":")[1].split(",")
            self.sht_temp_label.configure(text=f"Temperature: {sht_readings[0]} C")
            self.sht_humidity_label.configure(text=f"Humidity: {sht_readings[1]} %")
        elif serial_input.startswith("Grove"):
            grove_readings = serial_input.split(":")[1].split(",")
            self.grove_label_1.configure(text=f"Nitrogen Dioxide: {grove_readings[0]} ppm / {grove_readings[1]} V")
            self.grove_label_2.configure(text=f"Alcohol Gas: {grove_readings[2]} ppm / {grove_readings[3]} V")
            self.grove_label_3.configure(text=f"VOC: {grove_readings[4]} ppm / {grove_readings[5]} V")
            self.grove_label_4.configure(text=f"Carbon Monoxide: {grove_readings[6]} ppm / {grove_readings[7]} V")

    def on_closing(self):
        self.serial_reader.stop()
        self.root.destroy()
