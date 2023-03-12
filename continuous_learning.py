import openai
from generator import generate_prompt,get_code_from_openai
from util import say
import requests
import json

messages = [{"role": "system", "content": "You are a helpful assistant."}]

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
fix_error = ""

say("What do you want me to do?")
baseline_objective = input("")
messages.append({ "role": "user", "content": generate_prompt(manifest, baseline_objective) })

# print(messages)
completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
code = get_code_from_openai(completion)

say("See what I have come up with:")
print(code)
say("Let's see if it compiles..")

def flashSketch(code):
    headers = {
        'Content-Type': 'application/json'
    }
    code_listing = code
    response = requests.post(
        "http://172.24.252.165:3000/flash", 
        data=json.dumps({ "code_listing": code_listing }), 
        headers=headers
    )
    return response

error_message = flashSketch(code)
if error_message != "":
    say("Oh no. I did something wrong. :(")
    say("Let me try to fix this..")
    fix_error = 'fix error: "' + error_message + '"'

bot_message = completion["choices"][0]["message"]
messages.append(bot_message)


while True:
    changes = ""
    if fix_error == "":
        say("Is there anything I should change?")
        changes = input("")
    else :
        changes = fix_error
        fix_error = ""

    messages.append({ "role": "user", "content": "make changes: " + changes })
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    bot_message = completion["choices"][0]["message"]
    code = get_code_from_openai(completion)
    messages.append(bot_message)
    error_message = flashSketch(code)
    if error_message != "":
        say("Oh no. I did something wrong. :(")
        say("Let me try to fix this..")
        fix_error = 'fix error: "' + error_message + '"'

