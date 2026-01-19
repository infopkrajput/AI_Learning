from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import re

load_dotenv()

client = genai.Client()

system_prompt = f"""
    You are an helpful AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns output
    
    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""

def get_weather(city):
    weather_data = {
        "new york": "12 Degree Cel",
        "london": "8 Degree Cel",
        "paris": "10 Degree Cel"
    }
    return weather_data.get(city.lower(), "Not available in Database")

def run_command(command):
    return f"Executed: {command}"

print("Weather Agent (type 'exit' to quit)")

while True:
    user_input = input("> ")
    if user_input.lower() in ["exit", "quit"]:
        break
    current_input = user_input
    while True:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt),
            contents=current_input
        )
        print("Gemini:", response.text)
        try:
            match = re.search(r'\{.*?\}', response.text, re.DOTALL)
            if not match:
                break
            json_str = match.group(0)
            ai_json = json.loads(json_str)
        except Exception as e:
            print("[Error parsing AI response as JSON]", e)
            break
        if ai_json.get("function") == "get_weather":
            city = ai_json.get("input", "")
            weather = get_weather(city)
            print(f"[Tool] get_weather('{city}') => {weather}")
            current_input = json.dumps({"step": "observe", "output": weather})
            continue
        elif ai_json.get("function") == "run_command":
            command = ai_json.get("input", "")
            output = run_command(command)
            print(f"[Tool] run_command('{command}') => {output}")
            current_input = json.dumps({"step": "observe", "output": output})
            continue
        if ai_json.get("step") in ["output", "result"]:
            print(f"[Final Answer] {ai_json.get('content', '')}")
            break
        current_input = json.dumps(ai_json)