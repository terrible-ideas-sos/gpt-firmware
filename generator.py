import openai
import os
from dotenv import load_dotenv
from arduinointerface import flashSketch, startHandlingSerialData

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_code_block_from_text(text):
    try:
      start = text.find("```")
      end = text.find("```", start + 3)
      code = text[start + 3:end]
      # check if first line is "arduino", "c" or "c++"
      # case insensitve
      if code.splitlines()[0].lower() in ["arduino", "c", "c++"]:
          # remove first line
          code = code.splitlines()[1:].join("\n")
    except Exception as e:
      print('Error extracting code block from text: ', e)
      print("Text: ", text)
    return code

def get_code_from_openai(completion):
  message = completion["choices"][0]["message"]["content"]
  code = extract_code_block_from_text(message)
  return code


def generate_firmware_and_flash(manifest, objective):
  print("Getting ChatGPT API response...")

  prompt = """Write an arduino sketch.

{manifest}

The objective of the arduino is: {objective}"""
  prompt = prompt.format(manifest=manifest,objective=objective)

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

if __name__ == "__main__":

  manifest =   """Use 115200 baud rate. 
  Measure the brightness using a photosensor connected to pin A7 as analog input. 
  Use an LED connected to pin 3 as analog output. 
  """

  generate_firmware_and_flash(manifest, "Start by turning the LED off. Then slowly increase the LED output every 250ms until the photosensor measures 750. When reaching 750 keep the led on. Output the led value and photosensor value on the serial port everytime the led value is increased.")
  simple_serial_start()