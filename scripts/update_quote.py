#!/usr/bin/env python3
"""
Pick a random quote of the day and write shields.io-compatible JSON
to data/quote.json  (schemaVersion 1)
"""
import json, os, random, datetime, pathlib

QUOTES_FILE = pathlib.Path("quotes.json")           # ← Pfad ggf. anpassen
TARGET_FILE = pathlib.Path("data/quote.json")

def main() -> None:
    quotes = json.loads(QUOTES_FILE.read_text(encoding="utf-8"))
    quote = random.choice(quotes)

    payload = {
        "schemaVersion": 1,
        "label": "Quote",
        "message": quote,
        "color": "yellow",
        "labelColor": "555",
    }
    TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    TARGET_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"[{datetime.datetime.utcnow().isoformat()}] wrote quote: {quote}")

if __name__ == "__main__":
    main()
