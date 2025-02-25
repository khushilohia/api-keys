from fastapi import FastAPI, Request, HTTPException
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import secrets

app = FastAPI()

# Generate and Store an API Key
API_KEY = secrets.token_hex(16)
print(f"Your API Key: {API_KEY}")  # Store this safely!

# Load a lightweight summarization model (DistilBART for speed)
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16)

@app.post("/summarize")
async def summarize(request: Request):
    try:
        # API Key Authentication
        user_api_key = request.headers.get("x-api-key")
        if user_api_key != API_KEY:
            raise HTTPException(status_code=403, detail="Invalid API key")

        # Get input text
        data = await request.json()
        input_text = data.get("text", "")

        if not input_text:
            raise HTTPException(status_code=400, detail="No text provided")

        # Tokenize & Summarize
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding="longest")
        summary_ids = model.generate(**inputs, max_length=60, min_length=20, length_penalty=2.0)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
