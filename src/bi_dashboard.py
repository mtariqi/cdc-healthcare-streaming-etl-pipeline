import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URL, PROCESSED_DATA_DIR


def generate_bi_summary():
    engine = create_engine(DATABASE_URL)

    query = """
    SELECT
        year,
        stateabbr,
        measure,
        ROUND(AVG(data_value)::numeric, 2) AS avg_value,
        MIN(data_value) AS min_value,
        MAX(data_value) AS max_value,
        COUNT(*) AS record_count
    FROM cdc_places_health_indicators
    GROUP BY year, stateabbr, measure
    ORDER BY avg_value DESC;
    """

    df = pd.read_sql(query, engine)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DATA_DIR / "bi_health_indicator_summary.csv"

    df.to_csv(output_file, index=False)

    print("BI summary created successfully")
    print(df.head(10))
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_bi_summary()
