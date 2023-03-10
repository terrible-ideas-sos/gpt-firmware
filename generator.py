import openai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

text = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "write an arduino c listing for a robot"},
    ]
)

print(text)