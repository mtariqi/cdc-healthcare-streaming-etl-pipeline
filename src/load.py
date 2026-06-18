import pandas as pd
from sqlalchemy import create_engine


def load_to_postgres(df: pd.DataFrame, database_url: str, table_name: str) -> None:
    engine = create_engine(database_url)

    with engine.begin() as connection:
        df.to_sql(
            table_name,
            connection,
            if_exists="append",
            index=False,
            method="multi"
        )

    print(f"Loaded {len(df)} records into table: {table_name}")


if __name__ == "__main__":
    from extract import extract_cdc_data
    from transform import transform_cdc_data
    from validate import validate_cdc_data
    from config import DATABASE_URL, TARGET_TABLE

    raw_df = extract_cdc_data(limit=10)
    clean_df = transform_cdc_data(raw_df)
    validate_cdc_data(clean_df)
    load_to_postgres(clean_df, DATABASE_URL, TARGET_TABLE)
