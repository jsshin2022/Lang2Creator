
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import requests

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class UserQuery(BaseModel):
    user: str
    text: str

@app.post("/ask")
async def ask_agent(query: UserQuery):
    prompt = f"""You are a command router. Recognize the user input and decide which agent to forward to.
Supported agents:
- youtube-agent

User said: "{query.text}"
Return: {{ "route": "youtube-agent", "payload": {{...}} }}
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    parsed = eval(response.choices[0].message.content)

    if parsed["route"] == "youtube-agent":
        try:
            resp = requests.post("http://localhost:5001/youtube", json=parsed["payload"])
            return resp.json()
        except Exception as e:
            return {"error": f"Agent not reachable: {e}"}
    return {"error": "Unsupported route"}
