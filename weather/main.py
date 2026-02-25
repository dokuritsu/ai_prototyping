import json
from weather import get_weather
from openai import OpenAI

# Trying to utilize external API data (current weather) and feed it into the OpenAI model for analysis. 1. Pull read data from API 2. Feed into LLM. 3. Produced structured analysis
client = OpenAI()

SYSTEM = """You are a practical assistant.
You must follow this process:
1) Decide if you need weather data to answer.
2) If you need weather, output ONLY a JSON object with:
   {"action":"get_weather","latitude":<float>,"longitude":<float>,"question":"..."}
3) If you do NOT need weather, output ONLY:
   {"action":"answer","answer":"...", "confidence":0-1}

After weather is provided, output ONLY:
{"action":"answer","answer":"...", "confidence":0-1, "why":"..."}.
Keep answers concise.
"""

def ask_openai(messages):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return resp.choices[0].message.content

def validate_decision (text):
    try:
        # Confirms valid json
        data = json.loads(text)

        # Confirms "action" is structured into json
        if "action" not in data:
            return False, None
        # Confirms "get_weather" is correctly accompanied by "latitude" & "longitude"
        if data["action"] == "get_weather":
            if "latitude" not in data or "longitude" not in data:
                return False, None
            
        return True, data
    except json.JSONDecodeError:
        return False, None

def main():
    user_question = input("Ask a question: ").strip()

    # 1) Ask the model what to do
    first = ask_openai([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_question}
    ])

    valid, decision = validate_decision(first)
    if not valid:
            print("Invalid decision from model")
            print(first)
            return
    
    if decision.get("action") == "get_weather":
        print("\nDecision step:")
        print(json.dumps(decision, indent=2))
        lat = float(decision["latitude"])
        lon = float(decision["longitude"])
    
        weather = get_weather(lat, lon)

        # 2) Give weather back and ask for final answer
        final = ask_openai([
            {"role": "system", "content": SYSTEM}, 
            {"role": "user", "content": user_question}, 
            {"role": "assistant", "content": json.dumps(decision)},
            {"role": "user", "content": f"Here is the weather data JSON:\n{json.dumps(weather)}"}
        ])

        print(final)

    elif decision.get("action") == "answer":
        print(json.dumps(decision, indent=2))
    else:
        print("Unexpected action. Raw JSON:\n", json.dumps(decision, indent=2))

if __name__ == "__main__":
    main()
