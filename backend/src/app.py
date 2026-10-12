from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from database import get_page, page_response, save_checked_page
from scraper import normalize_url, scrape_page


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
    data = request.get_json(silent=True) or {}
    url = data.get("url","")

    if not isinstance(url,str) or not url.strip():
        return jsonify({"error" :"Please enter a url"}) , 400

    try:
        url = normalize_url(url)
        saved = get_page(url)
        if saved:
            return jsonify(page_response(saved))

        save_checked_page(url, scrape_page(url))
        return jsonify(page_response(get_page(url), cached = False))

    except ValueError as error:
        return jsonify({"error" : str(error)}), 400
    except Exception:
        app.logger.exception("Could not fetch or save the page")
        return jsonify({"error": "Could not fetch or save this page right now."}), 502


if __name__ == "__main__":
    app.run(debug=True)
