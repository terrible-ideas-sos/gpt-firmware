from everywhereml.arduino import Sketch, Ino, H
import threading
from dotenv import load_dotenv
from threading import Timer
import serial
import time
import os

load_dotenv()

# Configuration
conf_sketchname = 'terribleSketch'
conf_board = 'Mega 2560'
conf_serialport = os.getenv("SERIAL_PORT")
conf_baudrate = 115200


# Flash an arduino board with code, optionally specify board type, sketchname and serial port
def flashSketch(sketchcode, sketechname=conf_sketchname, boardtype=conf_board, portname=conf_serialport):
    # Create a sketch with the configured sketch name
    sketch = Sketch(name=sketechname, folder=":system:")

    # Add code to sketch
    sketch += Ino(sketchcode)

    # Compile sketch for configured board
    if sketch.compile(board=boardtype).is_successful:
        print('Log', sketch.output)
        print('Sketch stats', sketch.stats)
    else:
        print('ERROR', sketch.output)

    # Upload it to the configured port
    sketch.upload(port=portname)

    print(sketch.output)

# Handle serial output of arduino
serialport_connected = False
serial_port = serial.Serial(conf_serialport, conf_baudrate, timeout=0)
_serialPortHandlerThread = None
_stopReadingSerialPort = False

def _read_from_serialport(ser, callback):
    global serialport_connected, _stopReadingSerialPort
    while not serialport_connected and not _stopReadingSerialPort:
        #serin = ser.read()
        serialport_connected = True

        while True and not _stopReadingSerialPort:
           reading = ser.readline().decode()
           if(reading != ""): # If not empty handle
            callback(reading)

def startHandlingSerialData(dataHandlerCallback, stopAfterTime_secs = None):
    global _serialPortHandlerThread, _stopReadingSerialPort
    if _serialPortHandlerThread == None:
        _stopReadingSerialPort = False
        _serialPortHandlerThread = threading.Thread(target=_read_from_serialport, args=(serial_port, dataHandlerCallback,))
        _serialPortHandlerThread.start()

        if (stopAfterTime_secs is not None):
            st = Timer(stopAfterTime_secs, stopHandlingSerialData, ())
            st.start()

    else:
        print("ERROR", "Active serial data handler thread.")
        print("You may want to call stopHandlingSerialData before calling startHandlingSerialData again.")
    
def stopHandlingSerialData():
    global _serialPortHandlerThread, _stopReadingSerialPort
    _stopReadingSerialPort = True # Run out of serial port reading loop
    _serialPortHandlerThread.join() # Wait thread to finish
    _serialPortHandlerThread = None # Clean up

#######################
#######################
# EXAMPLE TEST
# Flashes an arduino sketch that prints meow every second, then reads it out at the serial port

code = """
        void hello() {
            Serial.println("meow");
        }


        void setup() {
            Serial.begin(115200);
        }

        void loop() {
            hello();
            delay(1000);
        }
    """

# Handler that can passed as callback to receive serial data async
def serialDataHandler(data):
    # Simply outputs what it reads at the serial port
    print(data, end = '')

if __name__ == "__main__":
    # Actual code
    print("Flashing Arduino Sketch..")
    flashSketch(code)

    print("Reading Serial Port for 3 seconds:")
    startHandlingSerialData(serialDataHandler, stopAfterTime_secs=3)

# #
# #######################
# #######################
