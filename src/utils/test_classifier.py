from pathlib import Path

from src.data.email_parser import parse_email_bytes
from src.utils.classifier import classify_email


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SPAM_DIR = PROJECT_ROOT / "data" / "raw" / "spam"


def main():

    print("=" * 60)
    print("REAL EMAIL CLASSIFIER ROUTING TEST")
    print("=" * 60)

    # Pick the first real spam email from the dataset
    spam_files = [
        file for file in SPAM_DIR.iterdir()
        if file.is_file()
    ]

    email_file = spam_files[10]

    print(f"\nTesting file: {email_file.name}")

    # Read raw .eml
    with open(email_file, "rb") as file:
        email_bytes = file.read()

    # Parse using the same parser used by the API
    email_data = parse_email_bytes(email_bytes)

    print(f"Subject: {email_data['subject']}")

    # Classify and route
    result = classify_email(
        email_data["subject"],
        email_data["body"]
    )

    print("\nCLASSIFICATION RESULT")
    print(result)

    print("\nCheck:")
    print("data/quarantine/quarantine.csv")
    print("for the quarantined email.")


if __name__ == "__main__":
    main()