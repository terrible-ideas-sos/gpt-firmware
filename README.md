# ChatGPT firmware-flashing Arduino robot


## Sample ChatGPT output

```c++
#include <MeOrion.h>   // Include Makeblock Library SDK

// Declare motors and sensors
MeDCMotor leftmotor(M1);
MeDCMotor rightmotor(M2);
MePort port(PORT_3);
Servo clawservo;
int16_t clawservopin = port.pin1();
MeUltrasonicSensor ultraSensor(PORT_5);

void setup()
{
  // Attach claw servo to pin
  clawservo.attach(clawservopin);

  // Set motor speed and direction
  leftmotor.run(-200);   // Set left motor to move backward
  rightmotor.run(200);   // Set right motor to move forward
}

void loop()
{
  // Continue moving forward until distance sensor detects an obstacle
  if (ultraSensor.distanceCm() > 10)   // If no obstacle detected
  {
    // Do nothing and continue moving forward
  }
  else   // If obstacle detected
  {
    // Stop both motors and wait for 1 second
    leftmotor.stop();
    rightmotor.stop();
    delay(1000);

    // Open claw
    clawservo.write(0);
    delay(1000);

    // Reverse direction and continue moving forward with updated motor directions
    leftmotor.run(200);
    rightmotor.run(-200);
    delay(500);
  }
}
```

## Requirements

Make sure to install/update Arduino-CLI (on MacOS):

```
brew update
brew install arduino-cli
```

To work with Arduino Mega 2560, make sure to install the avr core using Arduino-CLI:

```
arduino-cli core install arduino:avr
```
