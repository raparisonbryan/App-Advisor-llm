from fastapi import FastAPI, Request
from transformers import pipeline

app = FastAPI()

generator = pipeline("text-generation", model="sshleifer/tiny-gpt2")

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    results = generator(
        prompt,
        max_new_tokens=100, 
        truncation=True,    
        pad_token_id=50256  
    )

    return {"output": results[0]["generated_text"]}
