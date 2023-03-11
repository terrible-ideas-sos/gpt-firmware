from generator import extract_code_block_from_text

test_case = """```c++
#include <MeMCore.h>

MeDCMotor motor1(M1);
MeDCMotor motor2(M2);

void setup() {
  Serial.begin(115200);
  motor1.run(0); // Stop motor1
  motor2.run(0); // Stop motor2
}

void loop() {
  motor1.run(100); // Set motor1 speed to +100% (forward)
  motor2.run(-100); // Set motor2 speed to -100% (forward)
}
```"""

print(extract_code_block_from_text(test_case))