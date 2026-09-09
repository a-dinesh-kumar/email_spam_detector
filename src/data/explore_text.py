from pathlib import Path
from collections import Counter
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "emails.csv"


def get_words(text):
    """Extract simple word tokens for exploration."""
    return re.findall(r"\b[a-zA-Z]{2,}\b", str(text).lower())


def main():

    df = pd.read_csv(DATA_FILE)

    print("=" * 60)
    print("TEXT EXPLORATION")
    print("=" * 60)

    # -----------------------------------------------------
    # 1. Average subject/body length by label
    # -----------------------------------------------------

    df["subject_length"] = df["subject"].fillna("").str.len()
    df["body_length"] = df["body"].fillna("").str.len()

    print("\nAverage lengths by label:")
    print(
        df.groupby("label")[["subject_length", "body_length"]]
        .mean()
        .round(2)
    )

    # -----------------------------------------------------
    # 2. Median lengths by label
    # -----------------------------------------------------

    print("\nMedian lengths by label:")
    print(
        df.groupby("label")[["subject_length", "body_length"]]
        .median()
        .round(2)
    )

    # -----------------------------------------------------
    # 3. Empty body by label
    # -----------------------------------------------------

    empty_body = (
        df["body"]
        .fillna("")
        .str.strip()
        .eq("")
    )

    print("\nEmpty body by label:")
    print(df.loc[empty_body, "label"].value_counts())

    # -----------------------------------------------------
    # 4. URL presence
    # -----------------------------------------------------

    df["contains_url"] = (
        df["body"]
        .fillna("")
        .str.contains(
            r"https?://|www\.",
            case=False,
            regex=True
        )
    )

    print("\nEmails containing URLs:")
    print(
        pd.crosstab(
            df["label"],
            df["contains_url"],
            normalize="index"
        ).round(3)
    )

    # -----------------------------------------------------
    # 5. HTML presence
    # -----------------------------------------------------

    df["contains_html"] = (
        df["body"]
        .fillna("")
        .str.contains(
            r"<[^>]+>",
            regex=True
        )
    )

    print("\nEmails containing HTML:")
    print(
        pd.crosstab(
            df["label"],
            df["contains_html"],
            normalize="index"
        ).round(3)
    )

    # -----------------------------------------------------
    # 6. Most common words
    # -----------------------------------------------------

    for label in ["ham", "spam"]:

        text = " ".join(
            df.loc[df["label"] == label, "body"]
            .fillna("")
        )

        words = get_words(text)

        counter = Counter(words)

        print(f"\nTop 20 words in {label.upper()}:")

        for word, count in counter.most_common(20):
            print(f"{word:20} {count}")

    # -----------------------------------------------------
    # 7. Subject examples
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("SAMPLE SUBJECTS")
    print("=" * 60)

    for label in ["ham", "spam"]:

        print(f"\n{label.upper()} subjects:")

        samples = (
            df.loc[df["label"] == label, "subject"]
            .dropna()
            .head(10)
        )

        for subject in samples:
            print(f"- {subject}")


if __name__ == "__main__":
    main()