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


def inspect_email(email_file):
    """Display the structure of one email."""

    message = parse_email(email_file)

    print("\n" + "=" * 70)
    print(f"FILE: {email_file}")
    print("=" * 70)

    print("\nHeaders:")
    print("From   :", message.get("From"))
    print("To     :", message.get("To"))
    print("Subject:", message.get("Subject"))

    print("\nOverall Structure:")
    print("Content Type :", message.get_content_type())
    print("Multipart    :", message.is_multipart())

    if message.is_multipart():

        print("\nMIME Parts:")

        for number, part in enumerate(message.walk(), start=1):

            # The root message itself is included by walk()
            if part.is_multipart():
                continue

            print(f"\nPart {number}")
            print("Content Type :", part.get_content_type())
            print("Content Disposition :", part.get("Content-Disposition"))

            try:
                content = part.get_content()

                print("Content Preview:")
                print(content[:500])

            except Exception as error:
                print("Could not extract content:", error)

    else:

        print("\nBody Preview:")

        try:
            content = message.get_content()
            print(content[:1000])

        except Exception as error:
            print("Could not extract body:", error)


def main():

    examples = {
        "Plain Text HAM": (
            RAW_DATA_DIR
            / "easy_ham"
            / "0001.ea7e79d3153e7469e7a9c3e0af6a357e"
        ),

        "HTML HAM": (
            RAW_DATA_DIR
            / "hard_ham"
            / "0001.f0cf04027e74802f09f723cb8916b48e"
        ),

        "Multipart HAM": (
            RAW_DATA_DIR
            / "easy_ham"
            / "0011.07b11073b53634cff892a7988289a72e"
        )
    }

    for name, email_file in examples.items():

        print(f"\n\n### {name} ###")

        if email_file.exists():
            inspect_email(email_file)
        else:
            print(f"File not found: {email_file}")


if __name__ == "__main__":
    main()