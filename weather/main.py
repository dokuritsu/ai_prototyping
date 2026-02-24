import sys
import weather
from openai import OpenAI

# Trying to utilize external API data (current weather) and feed it into the OpenAI model for analysis. 1. Pull read data from API 2. Feed into LLM. 3. Produced structured analysis
client = OpenAI()

user_input = weather.get_current_weather(41.85, -87.65)

response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages = [
        {"role": "system", "content": 'Analyze the following current weather and respond in the following JSON format: {{"risks": [], "recommendations": [], "summary": ""}}'},
        {"role": "user", "content": f"Analyze the current weather data:\n{user_input}"}
    ],
)

print("AI Response: " + response.choices[0].message.content)