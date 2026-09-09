from pathlib import Path
from email import policy
from email.parser import BytesParser


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw dataset directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def parse_email(email_file):
    """Parse a raw email file."""

    with open(email_file, "rb") as file:
        return BytesParser(policy=policy.default).parse(file)


def find_examples():
    """Find examples of different email structures."""

    examples = {
        "text/plain": None,
        "text/html": None,
        "multipart": None
    }

    folders = [
        RAW_DATA_DIR / "easy_ham",
        RAW_DATA_DIR / "hard_ham",
        RAW_DATA_DIR / "spam"
    ]

    for folder in folders:

        for email_file in folder.iterdir():

            if not email_file.is_file():
                continue

            try:
                message = parse_email(email_file)

                content_type = message.get_content_type()

                if (
                    content_type == "text/plain"
                    and examples["text/plain"] is None
                ):
                    examples["text/plain"] = email_file

                elif (
                    content_type == "text/html"
                    and examples["text/html"] is None
                ):
                    examples["text/html"] = email_file

                if (
                    message.is_multipart()
                    and examples["multipart"] is None
                ):
                    examples["multipart"] = email_file

            except Exception as error:
                print(f"Could not parse {email_file}: {error}")

    return examples


def main():

    examples = find_examples()

    print("\n===== Email Structure Examples =====")

    for email_type, email_file in examples.items():

        print(f"\n{email_type}")

        if email_file:
            print(f"Found: {email_file}")
        else:
            print("Not found")


if __name__ == "__main__":
    main()