from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")

@app.post("/generate")
async def generate_text(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=256)
    result = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"output": result}
