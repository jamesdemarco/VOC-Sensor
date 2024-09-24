import serial
import threading
import time

SERIAL_PORT = '/dev/cu.usbmodem14101'
BAUD_RATE = 9600


class SerialReader:
    def __init__(self, callback):
        self.serial_connection = None
        self.callback = callback
        self.running = True

        try:
            self.serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino : {e}")

    def start(self):
        threading.Thread(target=self.read_serial, daemon=True).start()

    def read_serial(self):
        while self.running:
            if self.serial_connection and self.serial_connection.is_open:
                line = self.serial_connection.readline().decode('utf-8').strip()
                if line:
                    self.callback(line)

    def stop(self):
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()