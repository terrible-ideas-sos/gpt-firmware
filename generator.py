import openai
import os
from dotenv import load_dotenv
from arduinointerface import flashSketch, startHandlingSerialData
from util import say

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_code_block_from_text(text):
    try:
      start = text.find("```")
      end = text.find("```", start + 3)
      code = text[start + 3:end]
      # check if first line is "arduino", "c" or "c++"
      # case insensitve
      # print("code",code)
      if code.splitlines()[0].lower() in ["arduino", "c", "c++", "cpp"]:
          # remove first line
          code = "\n".join(code.splitlines()[1:])
    except Exception as e:
      print('Error extracting code block from text: ', e)
      print("Text: ", text)
    return code

def get_code_from_openai(completion):
  message = completion["choices"][0]["message"]["content"]
  code = extract_code_block_from_text(message)
  return code

def generate_prompt(manifest, objective):
  say("Hmm.. Let me try to write the code for that...")

  prompt = """Write an arduino sketch with Makeblock.

{manifest}

The objective of the arduino is: {objective}"""
  prompt = prompt.format(manifest=manifest,objective=objective)
  return prompt

def generate_firmware_and_flash(manifest, objective):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": generate_prompt(manifest, objective)}
      ]
  )

  say("See what I came up with:")
  print(get_code_from_openai(completion))
  say("Let's see if it compiles..")

  flashSketch(get_code_from_openai(completion))

def serialDataHandler(data):
    # Simply outputs what it reads at the serial port
    print(data, end = '')

def simple_serial_start():
  startHandlingSerialData(serialDataHandler, stopAfterTime_secs=3000)

if __name__ == "__main__":

  manifest =   """Use 115200 baud rate. 
  """

  generate_firmware_and_flash(manifest, "Use the color sensor to sense the color and output the color via serial.")
  simple_serial_start()