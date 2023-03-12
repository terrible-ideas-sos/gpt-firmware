from everywhereml.arduino import Sketch, Ino, H
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from threading import Timer
import threading
import serial
import os

load_dotenv()

app = Flask(__name__)

# Configuration
conf_sketch_name = 'terribleSketch'
conf_board = 'Mega 2560'
conf_port = os.getenv("SERIAL_PORT")
conf_baudrate = 115200

# Flash an arduino board with code, optionally specify board type, sketch_name and serial port
def flash_sketch(sketch_code, sketch_name=conf_sketch_name, board=conf_board, port=conf_port):
    # Create a sketch with the configured sketch name
    sketch = Sketch(name=sketch_name, folder=":system:")

    # Add code to sketch
    sketch += Ino(sketch_code)

    # Compile sketch for configured board
    error_message = ""
    if sketch.compile(board=board).is_successful:
        print('Log', sketch.output)
        print('Sketch stats', sketch.stats)
    else:
        error_message = sketch.output
        print('ERROR', error_message)

    # Upload it to the configured port
    sketch.upload(port=port)

    print(sketch.output)
    return error_message

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
            _serial_port = serial.Serial(conf_port, conf_baudrate, timeout=0)

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

def serialDataHandler(data):
    # Simply outputs what it reads at the serial port
    print(data, end = '')

@app.route("/")
def home():
    return "I'm a ChatGPT robot!"


@app.route("/flash", methods=["POST"])
def code():
    code_listing = request.json["code_listing"]
    # do something with the code listing
    print("Code listing: ", code_listing)

    if _serialPortHandlerThread != None:
        stopHandlingSerialData()
    flash_sketch(code_listing)
    startHandlingSerialData(serialDataHandler)

    return jsonify({"status": "success", "code_listing": code_listing})

if __name__ == "__main__":
    app.run(debug=False, port=3000, host='0.0.0.0')