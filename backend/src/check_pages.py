from time import sleep

from database import init_db, list_pages, record_check_error, save_checked_page
from scraper import scrape_page


def main():
    init_db()
    pages = list_pages()
    changed = 0
    failed = 0

    for index, saved in enumerate(pages):
        if index:
            sleep(1)
        url = saved["url"]
        try:
            page = scrape_page(url)
            if save_checked_page(url, page):
                changed += 1
                print(f"CHANGED {url}")
            else:
                print(f"UNCHANGED {url}")
        except Exception as error:
            failed += 1
            record_check_error(url, error)
            print(f"ERROR {url}: {error}")

    print(f"Checked {len(pages)} page(s): {changed} changed, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
