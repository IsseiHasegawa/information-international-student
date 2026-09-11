from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from scraper import scrape_page


FRONTEND = Path(__file__).resolve().parents[2] / "frontend" / "src"
app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(FRONTEND, "index.html")


@app.route("/app.js")
def javascript():
    return send_from_directory(FRONTEND, "app.js")


@app.route("/api/scrape", methods=["POST"])
def scrape():
    data = request.get_json() or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "Please enter a URL."}), 400

    try:
        result = scrape_page(url)
        return jsonify(result)
    except Exception as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True)
