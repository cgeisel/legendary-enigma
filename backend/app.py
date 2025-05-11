from flask import Flask, request, jsonify
from flask_cors import CORS
from fuzzywuzzy import process
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Load the knowledge base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "data", "knowledge_base.json")

with open(KNOWLEDGE_BASE_PATH, "r") as f:
    knowledge_base = json.load(f)

# Set your OpenAI API key (ensure this is securely stored in an environment variable)

@app.route("/ask", methods=["POST"])
def ask_question():
    """
    Endpoint to handle user questions and return answers from the knowledge base.
    """
    user_query = request.json.get("query", "").lower()
    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    matches = process.extract(user_query, [entry["question"] for entry in knowledge_base], limit=5)

    if not matches:
        return jsonify({"message": "No relevant answers found."}), 404

    # Retrieve the matching entries with their scores
    matching_entries = [
        {"question": match[0], "score": match[1], "answer": next(
            entry["answer"] for entry in knowledge_base if entry["question"] == match[0]
        )}
        for match in matches if match[1] > 50  # Only include matches with a score > 50
    ]

    if not matching_entries:
        return jsonify({"message": "No relevant answers found."}), 404

    # Combine the retrieved answers into a single prompt for the generative model
    context = "\n".join([f"Q: {entry['question']}\nA: {entry['answer']}" for entry in matching_entries])
    prompt = f"The user asked: {user_query}\nBased on the following knowledge base, provide a detailed response:\n{context}"

    # Call the OpenAI API to generate a response using the updated ChatCompletion interface
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use a suitable model like gpt-3.5-turbo or gpt-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on a knowledge base."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7)
        generated_answer = response.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({"error": "Failed to generate a response", "details": str(e)}), 500

    return jsonify({
        "answers": matching_entries,
        "generated_answer": generated_answer
    })

if __name__ == "__main__":
    app.run(debug=True)