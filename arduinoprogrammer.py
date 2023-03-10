from everywhereml.arduino import Sketch, Ino, H

"""
Create a sketch object.
A sketch is defined by:
 - a name (required)
 - a folder (optional)

If you leave the folder empty, the current working directory will be used.
You can use the special name ':system:' to use the default Arduino sketches folder
(as reported by the command `arduino-cli config dump`)
"""

sketch = Sketch(name="PyDuino", folder=":system:")

"""
Then you can add files to the project (either the .ino main file or
C++ header files)
"""
sketch += Ino("""
    #include "hello.h"


    void setup() {
        Serial.begin(115200);
    }

    void loop() {
        hello();
        delay(1000);
    }
""")

sketch += ("hello.h", """
    void hello() {
        Serial.println("hello");
    }
""")


"""
Compile sketch for Arduino Nano 33 BLE board.
The board you target must appear in the `arduino-cli board listall` command.
If you know the FQBN (Fully Qualified Board Name), you can use that too.
"""
if sketch.compile(board='Nano 33 BLE').is_successful:
    print('Log', sketch.output)
    print('Sketch stats', sketch.stats)
else:
    print('ERROR', sketch.output)


"""
You can specify the exact port
"""
sketch.upload(port='/dev/ttyUSB0')

"""
Or even part of it.
The library will look for the best match.
"""
sketch.upload(port='ttyUSB')
sketch.upload(port='/dev/cu.usbmodem')

print(sketch.output)