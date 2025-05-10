from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load the knowledge base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "data", "knowledge_base.json")

with open(KNOWLEDGE_BASE_PATH, "r") as f:
    knowledge_base = json.load(f)

@app.route("/ask", methods=["POST"])
def ask_question():
    """
    Endpoint to handle user questions and return answers from the knowledge base.
    """
    user_query = request.json.get("query", "").lower()
    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # Basic search in knowledge base
    matching_entries = [
        entry for entry in knowledge_base if user_query in entry["question"].lower()
    ]

    if not matching_entries:
        return jsonify({"message": "No relevant answers found."}), 404

    return jsonify({"answers": matching_entries})

if __name__ == "__main__":
    app.run(debug=True)