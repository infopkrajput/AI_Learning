from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

cot_instruction = """
You are a logical assistant. Before answering any question, you must:
1. Analyze the user's request.
2. Break down the problem into smaller logical steps.
3. Solve each step sequentially.
4. Provide the final conclusion clearly.
"""

user_question = "If I have 3 apples and eat one, then buy two dozen more, how many do I have?"

print(f"User Question: {user_question}\n" + "-"*30)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=cot_instruction),
        contents=user_question
    )

    print(response.text)

except Exception as e:
    print(f"Error: {e}")