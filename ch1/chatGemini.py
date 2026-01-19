from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=[
        "You are a helpful assistant. which give me every output in poetic way.",  # system prompt (instruction)
        "Explain how AI works in a few words."  # user prompt
    ]
)

print(response.text)