import openai
from generator import generate_prompt,get_code_from_openai
from arduinointerface import flashSketch

messages = [{"role": "system", "content": "You are a helpful assistant."}]

manifest =   """
Use 115200 baud rate. 
Use Makeblock Library SDK.  
Use Makeblock LED matrix on Port 3.
For the main include, use #include <MeMCore.h>, instead of #include <MeOrion.h>
Use MeLEDMatrix class from the #include <MeLEDMatrix.h> for LED matrix.
Use `void drawBitmap(int8_t x, int8_t y, uint8_t Bitmap_Width, uint8_t *Bitmap)` method in MeLEDMatrix.
Use `void clearScreen()` method in MeLEDMatrix.
Left motor attached to `M1`. Going forward is positive value.
Right motor attached to `M2`. Going forward is negative value.
Use `void run(int speed)` method in MeDCMotor.
Use 250 as the speed.
"""
fix_error = ""

baseline_objective = input("Set the baseline objective: ")
messages.append({ "role": "user", "content": generate_prompt(manifest, baseline_objective) })

print(messages)
completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
code = get_code_from_openai(completion)
error_message = flashSketch(code)
if error_message != "":
    fix_error = "fix error: " + error_message
bot_message = completion["choices"][0]["message"]
messages.append(bot_message)

while True:
    changes = ""
    if fix_error == "":
        changes = input("What should be changed: ")
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
        fix_error = "fix error: " + error_message

