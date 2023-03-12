from generator import generate_firmware_and_flash, simple_serial_start

if __name__ == "__main__":

  manifest =   """
Use 115200 baud rate. 

Use Makeblock Library SDK.  

Declare MeDCMotor leftmotor(M1);
Declare MeDCMotor rightmotor(M2);

Declare MePort port(PORT_3)

Declare Servo clawservo;
Declare int16_t clawservopin = port.pin1();
Attach clawservo to clawservopin.

Declare MeUltrasonicSensor ultraSensor(PORT_5); 

"""

  generate_firmware_and_flash(manifest, "move forward using the left motor until you sense a value smaller than 50 with the ultrasonic sensor.")
  simple_serial_start()