import json
from scraper import fetch_and_parse_calendar

data = fetch_and_parse_calendar()
with open('news.json', 'w') as f:
    json.dump({'events': data}, f, indent=2)
