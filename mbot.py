from generator import generate_firmware_and_flash, simple_serial_start

if __name__ == "__main__":

  manifest =   """
Use 115200 baud rate. 

Use Makeblock Library SDK.  
For the main include, use #include <MeMCore.h>, instead of #include <MeOrion.h>

Declare MeDCMotor leftmotor(M1);
Declare MeDCMotor rightmotor(M2);

Declare MePort port(PORT_3)

Declare Servo clawservo;
Declare int16_t clawservopin = port.pin1();
Attach clawservo to clawservopin.

Declare MeUltrasonicSensor ultraSensor(PORT_5); 

Going forward for the right motor is positive value.
Going forward for the left motor is negative value.

"""

  generate_firmware_and_flash(manifest, "move forward until you sense a value smaller than 50 with the ultrasonic sensor. When sensing a value smaller than 50 set claw to 90 degrees. Otherwise set claw to 0 degrees.")
  simple_serial_start()