import openai
import os
from dotenv import load_dotenv
from arduinointerface import flashSketch, startHandlingSerialData

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_code_block_from_text(text):
    start = text.find("```")
    end = text.find("```", start + 3)
    code = text[start + 3:end]
    # check if first line is "arduino", "c" or "c++"
    # case insensitve
    if code.splitlines()[0].lower() in ["arduino", "c", "c++"]:
        # remove first line
        code = code.splitlines()[1:].join("\n")
    return code

def get_code_from_openai(completion):
  message = completion["choices"][0]["message"]["content"]
  code = extract_code_block_from_text(message)
  return code

print("Getting ChatGPT API response...")

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Use 115200 baud rate. Measure the brightness using a photosensor connected to pin A7 as analog input. Use an LED connected to pin A8 as analog output. Write an arduino sketch which sets the LED brightness to zero and then increases the LEDs brightness by 1 every 250 milliseconds until the photosensor reads a brightness level of 700. Always print out the brightness at the serial port and the led output value."}
    ]
)

print(get_code_from_openai(completion))

flashSketch(get_code_from_openai(completion))

def serialDataHandler(data):
    # Simply outputs what it reads at the serial port
    print(data, end = '')

startHandlingSerialData(serialDataHandler)