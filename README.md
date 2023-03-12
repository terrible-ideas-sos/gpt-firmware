# ChatGPT firmware-flashing Arduino robot
![IMG_4702](https://user-images.githubusercontent.com/2031472/224521842-18cb33e2-ca89-44d1-907d-dac636054761.jpg)
![IMG_4701](https://user-images.githubusercontent.com/2031472/224521844-2a5644e5-27d3-4708-8fd6-3fe7e24d086d.jpg)

## Introduction

Why write the Arduino code to control a robot when you can ask ChatGPT to do it for you?
And this is exactly what our team did at the Terrible Ideas Hackathon 2023 (https://terriblehack.nz). 


We used a Makeblock mBot (which basically uses an Arduino UNO as logic unit), attached a bunch of sensors and motors to it and asked ChatGPT to write code for us to perform simple tasks like: "Move forward and avoid obstacles."

As with microcontroller boards like Arduino UNOs the possibilities are basically endless, ChatGPT cannot make the magic happen out of no where. Therefore we tell ChatGPT once what sensors and actuators are attached to which ports. But that is basically it! The rest is up to ChatGPT and it gets directly compiled and uploaded to the mBot.

We were impressive to see how ChatGPT could sometimes produce flawless code that does exactly what we want. However, many other times.. it does the job 80% right and then gets something totally wrong. Thats why we implemented two features:

1. ChatGPT fixes compile errors itself. Yes really! We just feedback the error message and tell it to fix it. Often after another round it compiles flawlessly.
2. ChatGPT can improve the code according to the users wishes. After flashing and running the code the user can observe whether the robot does what it is supposed. Our system asks the user for an additional prompt to change any behaviour. We then just feed the existing code to ChatGPT again and ask ChatGPT to change the code to implement the new requested changes.

Thats it! Check out the photos, videos and code examples below to see how it works!


We would like to say thanks to the organisers and sponsors at the Terrible Ideas Hackathon 2023!

Cheers from our team SOS,
Alex, Jakes, Rongomai, Ilia, Moritz


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
