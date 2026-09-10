from pathlib import Path

from src.data.email_parser import parse_email_bytes


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EMAIL_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "spam"
    / "0003.4b3d943b8df71af248d12f8b2e7a224a"
)


def main():

    with open(EMAIL_FILE, "rb") as file:
        email_bytes = file.read()

    email_data = parse_email_bytes(email_bytes)

    print("=" * 60)
    print("EMAIL PARSER TEST")
    print("=" * 60)

    print("\nSubject:")
    print(email_data["subject"])

    print("\nBody preview:")
    print(email_data["body"][:500])

    print("\nBody length:", len(email_data["body"]))


if __name__ == "__main__":
    main()