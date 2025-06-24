from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("sshleifer/tiny-gpt2")
model = AutoModelForCausalLM.from_pretrained("sshleifer/tiny-gpt2")

@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(input_ids, max_length=100, num_return_sequences=1)

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"output": generated_text}
