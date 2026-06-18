import pandas as pd


def transform_cdc_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.lower().strip() for col in df.columns]

    selected_columns = [
        "year",
        "stateabbr",
        "statedesc",
        "locationname",
        "datasource",
        "category",
        "measure",
        "data_value",
        "data_value_unit",
        "data_value_type",
        "low_confidence_limit",
        "high_confidence_limit",
        "totalpopulation",
        "geolocation",
    ]

    available_columns = [col for col in selected_columns if col in df.columns]
    df = df[available_columns]

    numeric_columns = [
        "year",
        "data_value",
        "low_confidence_limit",
        "high_confidence_limit",
        "totalpopulation",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    text_columns = df.select_dtypes(include="object").columns

    for col in text_columns:
        df[col] = df[col].astype(str).str.strip()

    df = df.dropna(subset=["year", "stateabbr", "measure", "data_value"])

    return df


if __name__ == "__main__":
    from extract import extract_cdc_data

    raw_df = extract_cdc_data(limit=10)
    clean_df = transform_cdc_data(raw_df)

    print(clean_df.head())
    print(clean_df.dtypes)
