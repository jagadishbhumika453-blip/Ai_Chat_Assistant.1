from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Store conversation history
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    # Exit command
    if user_message.lower() in ["exit", "quit", "bye"]:
        chat_history.clear()
        return jsonify({
            "response": "Thank you for chatting! Have a nice day."
        })

    # Add user message
    chat_history.append(f"User: {user_message}")

    try:

        prompt = "\n".join(chat_history)

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        ai_reply = response.text

        # Save AI response
        chat_history.append(f"AI: {ai_reply}")

        return jsonify({
            "response": ai_reply
        })

    except Exception as e:
        return jsonify({
            "response": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)