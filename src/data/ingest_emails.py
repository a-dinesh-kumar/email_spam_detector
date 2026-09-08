from pathlib import Path
from email import policy
from email.parser import BytesParser

import pandas as pd


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "emails.csv"


# ---------------------------------------------------------
# Category → ML label mapping
# ---------------------------------------------------------

CATEGORY_TO_LABEL = {
    "easy_ham": "ham",
    "hard_ham": "ham",
    "spam": "spam",
}


# ---------------------------------------------------------
# Extract text from an email
# ---------------------------------------------------------

def extract_body(message):
    """
    Extract human-readable text from an email.

    We keep text/plain and text/html parts.
    Non-text MIME parts are ignored.
    """

    text_parts = []

    if message.is_multipart():

        for part in message.walk():

            content_type = part.get_content_type()

            if content_type not in ("text/plain", "text/html"):
                continue

            try:
                content = part.get_content()

                if content:
                    text_parts.append(content)

            except Exception:
                continue

    else:

        content_type = message.get_content_type()

        if content_type in ("text/plain", "text/html"):

            try:
                content = message.get_content()

                if content:
                    text_parts.append(content)

            except Exception:
                pass

    return "\n".join(text_parts).strip()


# ---------------------------------------------------------
# Process one email
# ---------------------------------------------------------

def process_email(email_file, category):

    with open(email_file, "rb") as file:

        message = BytesParser(
            policy=policy.default
        ).parse(file)

    subject = message.get("Subject", "")

    body = extract_body(message)

    label = CATEGORY_TO_LABEL[category]

    return {
        "id": email_file.name,
        "category": category,
        "label": label,
        "subject": subject,
        "body": body,
    }


# ---------------------------------------------------------
# Main ingestion pipeline
# ---------------------------------------------------------

def main():

    records = []

    parsing_failures = []

    print("Starting email ingestion...")
    print(f"Raw data directory: {RAW_DIR}")
    print()

    for category in CATEGORY_TO_LABEL:

        category_dir = RAW_DIR / category

        if not category_dir.exists():

            print(f"WARNING: Directory not found: {category_dir}")
            continue

        email_files = [
            file
            for file in category_dir.iterdir()
            if file.is_file()
        ]

        print(
            f"Processing {category}: "
            f"{len(email_files)} files"
        )

        for email_file in email_files:

            try:

                record = process_email(
                    email_file,
                    category
                )

                records.append(record)

            except Exception as error:

                parsing_failures.append(
                    {
                        "file": str(email_file),
                        "error": str(error),
                    }
                )

    # -----------------------------------------------------
    # Create DataFrame
    # -----------------------------------------------------

    df = pd.DataFrame(records)

    # -----------------------------------------------------
    # Create output directory
    # -----------------------------------------------------

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------
    # Save processed dataset
    # -----------------------------------------------------

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    # -----------------------------------------------------
    # Validation summary
    # -----------------------------------------------------

    print()
    print("=" * 60)
    print("INGESTION SUMMARY")
    print("=" * 60)

    print(f"Total records      : {len(df)}")
    print(f"Output file        : {OUTPUT_FILE}")
    print(
        f"Parsing failures   : "
        f"{len(parsing_failures)}"
    )

    if not df.empty:

        print()
        print("Records by category:")
        print(df["category"].value_counts())

        print()
        print("Records by label:")
        print(df["label"].value_counts())

        print()
        print(
            f"Missing subjects   : "
            f"{df['subject'].isna().sum()}"
        )

        print(
            f"Empty subjects     : "
            f"{(df['subject'].fillna('').str.strip() == '').sum()}"
        )

        print(
            f"Empty bodies       : "
            f"{(df['body'].fillna('').str.strip() == '').sum()}"
        )

        print()
        print(
            f"Duplicate IDs      : "
            f"{df['id'].duplicated().sum()}"
        )

    print("=" * 60)

    # -----------------------------------------------------
    # Parsing failures
    # -----------------------------------------------------

    if parsing_failures:

        print()
        print("Parsing failures:")

        for failure in parsing_failures:

            print(
                f"- {failure['file']}"
            )

            print(
                f"  Error: {failure['error']}"
            )


if __name__ == "__main__":
    main()