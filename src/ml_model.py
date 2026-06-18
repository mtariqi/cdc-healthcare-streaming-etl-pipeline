import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from config import DATABASE_URL, PROCESSED_DATA_DIR


def train_health_indicator_model():
    engine = create_engine(DATABASE_URL)

    query = """
    SELECT
        year,
        stateabbr,
        category,
        measure,
        data_value
    FROM cdc_places_health_indicators
    WHERE data_value IS NOT NULL;
    """

    df = pd.read_sql(query, engine)

    df = df.dropna(subset=["year", "stateabbr", "category", "measure", "data_value"])

    if len(df) < 20:
        raise ValueError("Not enough data to train model. Run main.py with more records first.")

    X = df[["year", "stateabbr", "category", "measure"]]
    y = df["data_value"]

    X_encoded = pd.get_dummies(X, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    results = pd.DataFrame({
        "actual": y_test.values,
        "predicted": predictions
    })

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DATA_DIR / "ml_predictions.csv"

    results.to_csv(output_file, index=False)

    print("Machine learning model completed")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"R2 Score: {r2:.2f}")
    print(results.head(10))
    print(f"Predictions saved to {output_file}")


if __name__ == "__main__":
    train_health_indicator_model()
