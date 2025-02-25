from flask import Flask, request, jsonify
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import torch
import secrets

app = Flask(__name__)

# Generate an API key (Store this securely)
API_KEY = secrets.token_hex(16)

# Load PEGASUS model
MODEL_NAME = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(MODEL_NAME)
model = PegasusForConditionalGeneration.from_pretrained(MODEL_NAME)

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # API Key Authentication
        user_api_key = request.headers.get("x-api-key")
        if user_api_key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 403

        # Get input text
        data = request.get_json()
        input_text = data.get("text", "")

        if not input_text:
            return jsonify({"error": "No text provided"}), 400

        # Tokenize & Summarize
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding="longest")
        summary_ids = model.generate(**inputs, max_length=60, min_length=20, length_penalty=2.0)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"Your API Key: {API_KEY}")  # Print the API Key
    app.run(host="0.0.0.0", port=5000, debug=True)
