import pandas as pd

from src.data.preprocess import clean_batch


INPUT_FILE = "data/processed/emails.csv"
OUTPUT_FILE = "data/processed/cleaned_emails.csv"


def main():

    df = pd.read_csv(INPUT_FILE)

    print(f"Total emails: {len(df)}")
    print("Cleaning emails...")

    df["cleaned_body"] = clean_batch(
        df["body"].fillna("").astype(str)
    )

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved cleaned data to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()