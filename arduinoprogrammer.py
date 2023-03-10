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
    void hello() {
        Serial.println("test");
    }


    void setup() {
        Serial.begin(115200);
    }

    void loop() {
        hello();
        delay(1000);
    }
""")



"""
Compile sketch for Arduino Nano 33 BLE board.
The board you target must appear in the `arduino-cli board listall` command.
If you know the FQBN (Fully Qualified Board Name), you can use that too.
"""
if sketch.compile(board='Mega 2560').is_successful:
    print('Log', sketch.output)
    print('Sketch stats', sketch.stats)
else:
    print('ERROR', sketch.output)


sketch.upload(port='/dev/cu.usbserial-14430')

print(sketch.output)