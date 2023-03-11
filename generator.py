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


def generate_firmware_and_flash(objective):
  print("Getting ChatGPT API response...")

  prompt = """Write an arduino sketch.

We have hc-sr04 sensor.
We use A0 as the trigger pin
We use A1 as echo pin.
We use 115200 baud rate.

The objective of the arduino is to '{objective}'"""
  prompt = prompt.format(objective=objective)

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": prompt}
      ]
  )

  print(get_code_from_openai(completion))

  flashSketch(get_code_from_openai(completion))

def serialDataHandler(data):
    # Simply outputs what it reads at the serial port
    print(data, end = '')

def simple_serial_start():
  startHandlingSerialData(serialDataHandler, stopAfterTime_secs=3000)

generate_firmware_and_flash("output hello world every 2 seconds on new line")
simple_serial_start()