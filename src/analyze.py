import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URL


def run_analysis():
    engine = create_engine(DATABASE_URL)

    query = """
    SELECT
        year,
        stateabbr,
        measure,
        ROUND(AVG(data_value)::numeric, 2) AS avg_value,
        COUNT(*) AS record_count
    FROM cdc_places_health_indicators
    GROUP BY year, stateabbr, measure
    ORDER BY avg_value DESC
    LIMIT 20;
    """

    df = pd.read_sql(query, engine)

    print("\nTop 20 Public Health Indicators by Average Value")
    print(df)

    df.to_csv("data/processed/health_indicator_analysis.csv", index=False)
    print("\nAnalysis saved to data/processed/health_indicator_analysis.csv")


if __name__ == "__main__":
    run_analysis()
