from html import unescape
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def clean_text(tag):
    text = tag.get_text(" ", strip=True)
    text = unescape(unescape(text))
    text = " ".join(text.split())

    return text


def scrape_page(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    domain = urlparse(url).netloc.lower()

    if domain != "uscis.gov" and not domain.endswith(".uscis.gov"):
        raise ValueError("Please use a USCIS.gov URL.")

    # Get the USCIS page
    response = requests.get(
        url,
        headers={"User-Agent": "StudentInfoProject/1.0"},
        timeout=10,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = ""
    if soup.title:
        title = clean_text(soup.title)

    # Work with the main part of the page
    content = soup.find("main")
    if content is None:
        content = soup

    # Remove page parts we do not need
    for item in content.find_all([
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "aside",
        "form",
        "button",
        "noscript",
        "svg",
    ]):
        item.decompose()

    # Keep content in the same order as the USCIS page
    page_content = []

    for element in content.find_all([
        "h1",
        "h2",
        "h3",
        "p",
        "ul",
        "ol",
        "table",
    ]):
        # Text inside a list or table will be handled by that list/table
        if element.name == "p" and element.find_parent(["ul", "ol", "table"]):
            continue

        # Do not add nested lists twice
        if element.name in ["ul", "ol"] and element.find_parent(["ul", "ol", "table"]):
            continue

        if element.name in ["h1", "h2", "h3"]:
            text = clean_text(element)

            if text:
                page_content.append({
                    "type": "heading",
                    "level": element.name,
                    "text": text,
                })

        elif element.name == "p":
            text = clean_text(element)

            if text:
                page_content.append({
                    "type": "paragraph",
                    "text": text,
                })

        elif element.name in ["ul", "ol"]:
            items = []

            for item in element.find_all("li", recursive=False):
                text = clean_text(item)

                if text:
                    items.append(text)

            if items:
                page_content.append({
                    "type": "list",
                    "list_type": element.name,
                    "items": items,
                })

        elif element.name == "table":
            rows = []

            for row in element.find_all("tr"):
                cells = []

                for cell in row.find_all(["th", "td"], recursive=False):
                    text = clean_text(cell)
                    cells.append(text)

                if cells:
                    rows.append(cells)

            if rows:
                page_content.append({
                    "type": "table",
                    "rows": rows,
                })

    # Keep useful links separate from the article content
    links = []
    seen_links = set()

    for link in content.find_all("a", href=True):
        text = clean_text(link)
        href = link["href"].strip()

        if not text or not href or href.startswith("#"):
            continue

        full_url = urljoin(response.url, href)
        link_key = (text, full_url)

        if link_key in seen_links:
            continue

        seen_links.add(link_key)
        links.append({
            "text": text,
            "url": full_url,
        })

    return {
        "title": title,
        "content": page_content,
        "links": links,
        "source": response.url,
    }
