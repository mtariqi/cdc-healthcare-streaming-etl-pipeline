import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URL, PROCESSED_DATA_DIR


def run_public_health_monitoring(threshold: float = 30.0):
    engine = create_engine(DATABASE_URL)

    query = f"""
    SELECT
        year,
        stateabbr,
        statedesc,
        locationname,
        measure,
        data_value
    FROM cdc_places_health_indicators
    WHERE data_value >= {threshold}
    ORDER BY data_value DESC;
    """

    alerts_df = pd.read_sql(query, engine)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DATA_DIR / "public_health_alerts.csv"

    alerts_df.to_csv(output_file, index=False)

    print(f"Public health monitoring completed")
    print(f"Alert threshold: {threshold}")
    print(f"Number of alerts: {len(alerts_df)}")
    print(alerts_df.head(10))
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    run_public_health_monitoring(threshold=30.0)
