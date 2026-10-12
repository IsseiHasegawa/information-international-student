from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from database import get_page, page_response, save_checked_page
from scraper import normalize_url, scrape_page
from summarizer import SummaryUnavailable, summarize_content


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
    url = data.get("url", "")

    if not isinstance(url, str) or not url.strip():
        return jsonify({"error": "Please enter a URL."}), 400

    try:
        url = normalize_url(url)
        saved = get_page(url)
        if saved:
            return jsonify(page_response(saved))

        save_checked_page(url, scrape_page(url))
        return jsonify(page_response(get_page(url), cached=False))

    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception:
        app.logger.exception("Could not fetch or save the page")
        return jsonify({"error": "Could not fetch or save this page right now."}), 502


@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")
    if not isinstance(url, str) or not url.strip():
        return jsonify({"error": "Please enter a URL first."}), 400

    try:
        saved = get_page(normalize_url(url))
        if saved is None:
            return jsonify({"error": "Save this page before requesting a summary."}), 404

        summary = summarize_content(saved["content_json"])
        return jsonify({"summary": summary})
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except SummaryUnavailable as error:
        return jsonify({"error": str(error)}), 503
    except Exception:
        app.logger.exception("Could not summarize the saved page")
        return jsonify({"error": "AI summary failed. Check the web logs and try again."}), 502


if __name__ == "__main__":
    app.run(debug=True)
