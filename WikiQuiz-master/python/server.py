import json
import requests

from flask import Flask, Response
from flask_cors import CORS

from urllib.parse import unquote

import wikipedia as wiki
from wikipedia.exceptions import PageError, DisambiguationError

from Article import Article


app = Flask(__name__)
CORS(app)


@app.route('/quiz/<path:article_name>/', methods=['GET'])
def get_quiz(article_name):
    try:
        if article_name.startswith("http"):
            if "/wiki/" in article_name:
                article_name = article_name.split("/wiki/")[-1]
            else:
                raise PageError(article_name)

        article_name = unquote(article_name)
        article_name = article_name.replace("_", " ")

        response_data = []

        article = Article(article_name)

        for question in article.quiz.get_ten_random():
            response_data.append((question.text, question.gaps))

        data_send = json.dumps({
            "sentences": response_data,
            "propers": article.quiz.get_random_propers()
        })

        resp = Response(data_send, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp

    except DisambiguationError:
        return Response(
            json.dumps({
                "error": "Topic is ambiguous. Please use a more specific name or full Wikipedia URL."
            }),
            status=400,
            mimetype='application/json'
        )

    except PageError:
        return Response(
            json.dumps({
                "error": "Wikipedia page not found. Please check spelling or URL."
            }),
            status=404,
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({
                "error": "Internal server error",
                "details": str(e)
            }),
            status=500,
            mimetype='application/json'
        )


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
