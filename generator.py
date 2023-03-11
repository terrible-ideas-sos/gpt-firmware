import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

text = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write an arduino sketch that uses hc-sr04 ultrasonic sensor and provide the distance of the senor as output in the serial port."}
    ]
)

print(text)

def extract_code_block_from_text(text):
    start = text.find("```")
    end = text.find("```", start + 3)
    return text[start + 3:end]

message = text["choices"][0]["message"]["content"]

print(extract_code_block_from_text(message))