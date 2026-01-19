from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.
For the given user input, analyse the input and break down the problem step by step.
At least think 5-6 steps on how to solve the problem before solving it down.
The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.
Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".
Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query
Output Format:
{{ step: "string", content: "string" }}
"""

query = input("Enter your query: ")
contents = [query]

steps = ["analyse", "think", "output", "validate", "result"]
step_index = 0

while step_index < len(steps):
    step = steps[step_index]
    prompt = f"Step: {step}\nUser Query: {query}\nFollow the Output Format strictly."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=[prompt]
    )
    print(response.text)
    step_index += 1