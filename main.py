from fastapi import FastAPI, Request
from transformers import pipeline

app = FastAPI()

generator = pipeline("text-generation", model="sshleifer/tiny-gpt2")

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    results = generator(prompt, max_length=100, num_return_sequences=1)
    return {"output": results[0]["generated_text"]}
