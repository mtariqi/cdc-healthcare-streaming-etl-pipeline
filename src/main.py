from datetime import datetime, timezone

from extract import extract_cdc_data
from transform import transform_cdc_data
from validate import validate_cdc_data
from load import load_to_postgres
from config import DATABASE_URL, TARGET_TABLE, PROCESSED_DATA_DIR


def run_pipeline(limit: int = 1000, offset: int = 0):
    print("Starting CDC healthcare ETL pipeline")

    raw_df = extract_cdc_data(limit=limit, offset=offset)
    clean_df = transform_cdc_data(raw_df)
    validate_cdc_data(clean_df)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    processed_file = PROCESSED_DATA_DIR / f"cdc_places_clean_{timestamp}.csv"

    clean_df.to_csv(processed_file, index=False)

    load_to_postgres(clean_df, DATABASE_URL, TARGET_TABLE)

    print(f"Processed file saved to {processed_file}")
    print("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline(limit=100)
