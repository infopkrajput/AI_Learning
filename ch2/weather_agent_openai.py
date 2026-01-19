from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful weather assistant that provides accurate and concise weather information.",
        },
        {
            "role": "user",
            "content": "What's the weather like in New York City today?",
        },
    ],)
print(response.choices[0].message.content)