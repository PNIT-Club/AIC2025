from flask import Flask, request, url_for, jsonify, send_from_directory
from flask_cors import CORS
from ai_search.faiss_singleton import FaissSingleton
import glob, os
from pathlib import Path

# Map list
videoToId = {
    "L21_V001": "1tW5RmNNVzFumUu4jefHpHHQqTAdALMnW",
    "L21_V002": "1Ek1AWRWQGMRxXVIgEsUS_LpYl9p7tY-C",
    "L21_V003": "1vWr5OO5rJeYiG44Cm9KeREJZ99IluKn7",
    "L21_V004": "1lQHFTY7T1FDiDW4fBsstwjf860bDavP9",
}

app = Flask(__name__)
CORS(app) # Enables CORS for all routes and origins by default
instance = FaissSingleton().get_instance()

# Build absolute path to your images folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root/
IMAGE_DIR = os.path.join(BASE_DIR, "src", "res", "images")
TEMP_ENDPOINT = "http://localhost:5000"

@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

@app.route('/search')
def search():
    search_type = request.args.get('searchType')
    query = request.args.get('q')

    # Log it out
    app.logger.info(f"SearchType: {search_type}, Query: {query}")
    results = instance.search(search_type, query)

    results = [{
        "url": f"{TEMP_ENDPOINT}/images/{result}",
        "id": "1lQHFTY7T1FDiDW4fBsstwjf860bDavP9" # videoToId[result.split("/")[0]]
    } for result in results]

    return {
        "result": results
    }

@app.route('/health')
def health():
    return {
        "status": "ok",
    }


if __name__ == '__main__':
    app.run(debug=True)
