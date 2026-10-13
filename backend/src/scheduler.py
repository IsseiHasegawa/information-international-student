import os
import time
from datetime import datetime, time as midnight, timedelta
from zoneinfo import ZoneInfo

from check_pages import main as check_pages
from database import init_db


def next_midnight(now, zone):
    local_now = now.astimezone(zone)
    return datetime.combine(local_now.date() + timedelta(days=1), midnight.min, tzinfo=zone)


def main():
    zone = ZoneInfo(os.getenv("CHECK_TIMEZONE", "America/Chicago"))
    init_db()
    print(f"Daily checker started; midnight time zone: {zone.key}", flush=True)

    while True:
        now = datetime.now(zone)
        due = next_midnight(now, zone)
        print(f"Next check: {due.isoformat()}", flush=True)
        while True:
            remaining = due.timestamp() - datetime.now(zone).timestamp()
            if remaining <= 0:
                break
            time.sleep(min(remaining, 60))
        try:
            check_pages()
        except Exception as error:
            print(f"Daily check failed: {error}", flush=True)


if __name__ == "__main__":
    main()
