from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "emails.csv"


def main():

    df = pd.read_csv(DATA_FILE)

    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nLabel distribution:")
    print(df["label"].value_counts())

    print("\nLabel distribution (%):")
    print(
        (df["label"].value_counts(normalize=True) * 100)
        .round(2)
    )

    print("\nCategory distribution:")
    print(df["category"].value_counts())

    print("\nSubject length statistics:")
    subject_length = df["subject"].fillna("").str.len()
    print(subject_length.describe())

    print("\nBody length statistics:")
    body_length = df["body"].fillna("").str.len()
    print(body_length.describe())

    print("\nBody length by label:")
    print(
        df.assign(
            body_length=df["body"].fillna("").str.len()
        )
        .groupby("label")["body_length"]
        .describe()
    )


if __name__ == "__main__":
    main()