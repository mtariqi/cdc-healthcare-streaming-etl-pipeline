import requests
import pandas as pd
from datetime import datetime, timezone

from config import CDC_API_URL, RAW_DATA_DIR


def extract_cdc_data(limit: int = 1000, offset: int = 0) -> pd.DataFrame:
    params = {
        "$limit": limit,
        "$offset": offset,
        "$order": ":id"
    }

    response = requests.get(CDC_API_URL, params=params, timeout=30)
    response.raise_for_status()

    df = pd.DataFrame(response.json())

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    raw_file = RAW_DATA_DIR / f"cdc_places_raw_{timestamp}.json"

    df.to_json(raw_file, orient="records", lines=True)

    print(f"Extracted {len(df)} records")
    print(f"Saved raw data to {raw_file}")

    return df


if __name__ == "__main__":
    extract_cdc_data(limit=10)
