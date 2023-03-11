import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_code_block_from_text(text):
    start = text.find("```")
    end = text.find("```", start + 3)
    return text[start + 3:end]

def get_code_from_openai(completion):
  message = completion["choices"][0]["message"]["content"]
  code = extract_code_block_from_text(message)
  return code


completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write an arduino sketch that uses hc-sr04 ultrasonic sensor and provide the distance of the senor as output in the serial port."}
    ]
)

print(completion)

print(get_code_from_openai(completion))