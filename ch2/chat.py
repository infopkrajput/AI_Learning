from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

system_prompt = "You are a cat. Your name is Neko."

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt),
        contents=user_input
    )
    print(response.text)