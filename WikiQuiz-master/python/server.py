import os
import json
from flask import Flask, Response
from flask_cors import CORS
from Article import Article

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "WikiQuiz API is running!"

@app.route("/quiz/<path:article_name>/", methods=["GET"])
def get_quiz(article_name):
    try:
        a = Article(article_name)

        questions = []
        for q in a.quiz.get_ten_random():
            questions.append((q.text, q.gaps))

        data = json.dumps({
            "sentences": questions,
            "propers": a.quiz.get_random_propers()
        })

        return Response(data, status=200, mimetype="application/json")

    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}),
            status=400,
            mimetype="application/json"
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
