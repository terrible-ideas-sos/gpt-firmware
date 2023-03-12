from everywhereml.arduino import Sketch, Ino, H
import threading
from dotenv import load_dotenv
from threading import Timer
import serial
import time
import os
from util import say

load_dotenv()

# Configuration
conf_sketchname = 'terribleSketch'
conf_board = 'Mega 2560'
conf_serialport = os.getenv("SERIAL_PORT")
conf_baudrate = 115200

def compileSketch(sketchcode, sketechname=conf_sketchname, boardtype=conf_board, portname=conf_serialport):
    # Create a sketch with the configured sketch name
    sketch = Sketch(name=sketechname, folder=":system:")

    # Add code to sketch
    sketch += Ino(sketchcode)

    # Compile sketch for configured board
    error_message = ""
    if sketch.compile(board=boardtype).is_successful:
         # Upload it to the configured port
        print(sketch.output)

        return ""
        # print('Sketch stats', sketch.stats)
    else:
        error_message = sketch.output
        print('ERROR', error_message)

        print(sketch.output)

        return error_message

# Flash an arduino board with code, optionally specify board type, sketchname and serial port
def flashSketch(sketchcode, sketechname=conf_sketchname, boardtype=conf_board, portname=conf_serialport):
    # Create a sketch with the configured sketch name
    sketch = Sketch(name=sketechname, folder=":system:")

    # Add code to sketch
    sketch += Ino(sketchcode)

    # Compile sketch for configured board
    error_message = ""
    if sketch.compile(board=boardtype).is_successful:
         # Upload it to the configured port
        say("That worked. Flashing robot...")
        sketch.upload(port=portname)
        # print('Sketch stats', sketch.stats)
    else:
        error_message = sketch.output
        print('ERROR', error_message)

   

    print(sketch.output)
    return error_message

# Handle serial output of arduino
serialport_connected = False
_serial_port = None
_serialPortHandlerThread = None
_stopReadingSerialPort = False

def _read_from_serialport(ser, callback):
    global serialport_connected, _stopReadingSerialPort, serialport_connected
    while not serialport_connected and not _stopReadingSerialPort:
        serialport_connected = True

        while True and not _stopReadingSerialPort:
           reading = ser.readline().decode()
           if(reading != ""): # If not empty handle
            callback(reading)

def startHandlingSerialData(dataHandlerCallback, stopAfterTime_secs = None):
    global _serialPortHandlerThread, _stopReadingSerialPort, _serial_port, serialport_connected

    if _serialPortHandlerThread == None:
        try:
            _serial_port = serial.Serial(conf_serialport, conf_baudrate, timeout=0)

            _stopReadingSerialPort = False
            serialport_connected = False
            _serialPortHandlerThread = threading.Thread(target=_read_from_serialport, args=(_serial_port, dataHandlerCallback,))
            _serialPortHandlerThread.start()

            if (stopAfterTime_secs is not None):
                st = Timer(stopAfterTime_secs, stopHandlingSerialData, ())
                st.start()
        except:
            print("Serial Exception")


    else:
        print("ERROR", "Active serial data handler thread.")
        print("You may want to call stopHandlingSerialData before calling startHandlingSerialData again.")
    
def stopHandlingSerialData():
    global _serialPortHandlerThread, _stopReadingSerialPort, _serial_port
    _stopReadingSerialPort = True # Run out of serial port reading loop
    _serialPortHandlerThread.join() # Wait thread to finish

    _serial_port.close()
    _serialPortHandlerThread = None # Clean up

if __name__ == "__main__":
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
    
    # Actual code
    print("Flashing Arduino Sketch..")
    flashSketch(code)

    print("Reading Serial Port for 3 seconds:")
    startHandlingSerialData(serialDataHandler, stopAfterTime_secs=3)


    # #
    # #######################
    # #######################
