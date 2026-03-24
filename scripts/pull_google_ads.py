"""
Pull Google Ads campaign data from Windsor.ai REST API.

Usage:
    export WINDSOR_API_KEY="your-key-here"
    python scripts/pull_google_ads.py

Outputs: data/google_ads_daily.csv (full replace)
"""

import csv
import os
import sys
from datetime import datetime, timedelta
from urllib.parse import urlencode
from urllib.request import urlopen
import json

ACCOUNT_ID = "856-857-0099"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "google_ads_daily.csv")
WINDSOR_API_URL = "https://connectors.windsor.ai/all"

FIELDS = [
    "campaign",
    "campaign_id",
    "campaign_status",
    "campaign_type",
    "date",
    "impressions",
    "spend",
    "average_cpm",
    "clicks",
    "conversions",
]


def pull_data():
    api_key = os.environ.get("WINDSOR_API_KEY")
    if not api_key:
        print("Error: WINDSOR_API_KEY environment variable is not set.", file=sys.stderr)
        print("Set it with: export WINDSOR_API_KEY='your-key-here'", file=sys.stderr)
        sys.exit(1)

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    params = {
        "api_key": api_key,
        "connector": "google_ads",
        "account_id": ACCOUNT_ID,
        "fields": ",".join(FIELDS),
        "date_preset": "custom",
        "start_date": start_date,
        "end_date": end_date,
    }

    url = f"{WINDSOR_API_URL}?{urlencode(params)}"
    print(f"Fetching data from Windsor API ({start_date} to {end_date})...")

    with urlopen(url) as response:
        result = json.loads(response.read().decode())

    data = result.get("data", [])
    if not data:
        print("Warning: No data returned from Windsor API.", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in data:
            writer.writerow({field: row.get(field, "") for field in FIELDS})

    print(f"Wrote {len(data)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    pull_data()
