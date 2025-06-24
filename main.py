from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

HF_API_URL = "https://api-inference.huggingface.co/models/sshleifer/tiny-gpt2"
HF_API_KEY = os.getenv("HF_API_KEY")

@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    response = requests.post(
        HF_API_URL,
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        return {"error": response.text}

    return {"output": response.json()}
