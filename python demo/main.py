import sys
from openai import OpenAI

# Providing a structured analysis based on the user input

client = OpenAI()

# Get text from the command line
if len(sys.argv) < 2:
    print("Please provide a text to summarize.")
    sys.exit(1)

user_input = sys.argv[1]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": 'Respond in the following JSON format: {"risks": [], "opportunities": [], "summary": ""}. Fill the "risk" array with potential risks of AI prototyping, '
        '"opportunities"array with potential opportunities of AI prototyping, etc'},
        {"role": "user", "content": f"Analyze the following text:\n{user_input}"}
    ],
)

# Write the response to a text file
with open("response.txt", "a", encoding="utf-8") as f:
    f.write(f"User Input: {user_input}\n")
    f.write(f"AI Response: {response.choices[0].message.content}\n")
    f.write(f"AI Usage: {response.usage}\n")

print("AI Response: " + response.choices[0].message.content)
print("AI Usage: " + str(response.usage))
# print(response)