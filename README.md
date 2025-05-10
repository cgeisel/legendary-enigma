# Shadowdark RPG QA System

This repository contains the prototype for a question-answering system about the Shadowdark RPG. It allows users to ask questions and retrieve relevant answers from a knowledge base of Shadowdark RPG rules, FAQs, and mechanics.

## Features

- Flask-based backend for processing user queries.
- Simple knowledge base in JSON format.
- REST API endpoint to fetch answers.

## Project Structure

```
shadowdark-prototype/
├── backend/
│   ├── app.py          # Backend application logic
│   ├── data/
│   │   └── knowledge_base.json  # Knowledge base for Shadowdark RPG
├── README.md           # Project documentation
├── .gitignore          # Ignored files and directories
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Flask

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/shadowdark-rpg-qa.git
   cd shadowdark-rpg-qa/backend
   ```

2. Install dependencies:
   ```bash
   pip install flask
   ```

3. Run the server:
   ```bash
   python app.py
   ```

4. Test the API:
   Use a tool like `curl` or Postman to send a POST request to the `/ask` endpoint.

### Example Request
```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "How do I create a Shadowdark RPG character?"}' http://127.0.0.1:5000/ask
```

### Example Response
```json
{
    "answers": [
        {
            "question": "How do I create a Shadowdark RPG character?",
            "answer": "To create a character, roll 3d6 for each ability score, select a class, and choose starting equipment."
        }
    ]
}
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.