from html import unescape
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def clean_text(tag):
    text = tag.get_text(" ", strip=True)
    text = unescape(text)
    text = " ".join(text.split())

    return text


def scrape_page(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    domain = urlparse(url).netloc.lower()

    if domain != "uscis.gov" and not domain.endswith(".uscis.gov"):
        raise ValueError("Please use a USCIS.gov URL.")

    # Make the request to the URL
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

    # Try to find USCIS main article area
    content = soup.find("main")

    if content is None:
        content = soup


    # Remove things we do not want
    for item in content.find_all([
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "aside",
        "form",
        "button"
    ]):
        item.decompose()

    # HEADINGS
    headings = []

    for heading in content.find_all(["h1", "h2", "h3"]):

        text = clean_text(heading)

        if text:
            headings.append(text)


    # PARAGRAPHS
    paragraphs = []

    for paragraph in content.find_all("p"):

        text = clean_text(paragraph)

        if len(text) > 40:
            paragraphs.append(text)

    # TABLES
    tables = []

    for table in content.find_all("table"):
        rows = []

        for row in table.find_all("tr"):
            cells = []

            for cell in row.find_all(["th", "td"]):
                text = clean_text(cell)
                cells.append(text)

            if cells:
                rows.append(cells)

        if rows:
            tables.append(rows)

    lists = []

    for list_tag in content.find_all(["ul", "ol"]):

        items = []

        for item in list_tag.find_all("li"):
            text = clean_text(item)

            if text:
                items.append(text)

        if items:
            lists.append(items)

    # LINKS
    links = []

    for link in content.find_all("a", href=True):

        text = clean_text(link)

        if not text:
            continue

        full_url = urljoin(
            response.url,
            link["href"]
        )

        links.append({
            "text": text,
            "url": full_url
        })

    # SEND EVERYTHING BACK
    return {
        "title": title,
        "headings": headings,
        "paragraphs": paragraphs,
        "lists": lists,
        "tables": tables,
        "links": links,
        "source": response.url,
    }