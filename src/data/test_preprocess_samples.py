import pandas as pd
from preprocess import clean_text


df = pd.read_csv("data/processed/emails.csv")

# Pick representative examples
samples = pd.concat([
    df[df["label"] == "ham"].head(3),
    df[df["label"] == "spam"].head(3)
])

for _, row in samples.iterrows():

    print("=" * 80)
    print(f"LABEL   : {row['label'].upper()}")
    print(f"SUBJECT : {row['subject']}")

    print("\nRAW BODY:")
    print(str(row["body"])[:1000])

    cleaned = clean_text(row["body"])

    print("\nCLEANED BODY:")
    print(cleaned[:1000])