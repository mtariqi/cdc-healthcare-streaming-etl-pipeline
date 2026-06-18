import pandas as pd


def validate_cdc_data(df: pd.DataFrame) -> bool:
    errors = []

    if df.empty:
        errors.append("Dataset is empty")

    required_columns = ["year", "stateabbr", "measure", "data_value"]

    for col in required_columns:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")

    if "year" in df.columns and df["year"].isnull().any():
        errors.append("Null year values found")

    if "stateabbr" in df.columns and df["stateabbr"].isnull().any():
        errors.append("Null state abbreviation values found")

    if "measure" in df.columns and df["measure"].isnull().any():
        errors.append("Null measure values found")

    if "data_value" in df.columns:
        if df["data_value"].isnull().any():
            errors.append("Null data_value values found")

        if (df["data_value"] < 0).any():
            errors.append("Negative data_value values found")

    if errors:
        raise ValueError(f"Data validation failed: {errors}")

    print("Data validation passed")
    return True


if __name__ == "__main__":
    from extract import extract_cdc_data
    from transform import transform_cdc_data

    raw_df = extract_cdc_data(limit=10)
    clean_df = transform_cdc_data(raw_df)
    validate_cdc_data(clean_df)
