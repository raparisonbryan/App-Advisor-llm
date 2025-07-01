from flask import Flask, request, jsonify
from huggingface_hub import InferenceClient
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN")
if not hf_token:
    raise EnvironmentError("HUGGINGFACE_HUB_TOKEN manquant dans les variables d'environnement")

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    api_key=hf_token
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message") if data else None

    if not user_input:
        return jsonify({"error": "Champ 'message' requis"}), 400

    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    return jsonify({"response": response.choices[0].message.content})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
