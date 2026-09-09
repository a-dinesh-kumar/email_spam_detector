from pathlib import Path
from email import policy
from email.parser import BytesParser


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw dataset directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def find_first_email(folder):
    """Find the first email file inside a folder."""

    for file in folder.iterdir():
        if file.is_file():
            return file

    return None


def parse_email(email_file):
    """Parse a raw email file."""

    with open(email_file, "rb") as file:
        message = BytesParser(policy=policy.default).parse(file)

    return message


def main():

    # We will inspect one HAM email first.
    ham_folder = RAW_DATA_DIR / "easy_ham"

    email_file = find_first_email(ham_folder)

    if email_file is None:
        print("No email files found.")
        return

    print("\n===== Email File =====")
    print(email_file)

    message = parse_email(email_file)

    print("\n===== Email Headers =====")

    print("From   :", message.get("From"))
    print("To     :", message.get("To"))
    print("Subject:", message.get("Subject"))
    print("Date   :", message.get("Date"))

    print("\n===== Email Structure =====")

    print("Content Type :", message.get_content_type())
    print("Is Multipart :", message.is_multipart())

    print("\n===== Email Body =====")

    if message.is_multipart():
        print("This email contains multiple parts.")
    else:
        body = message.get_content()
        print(body)


if __name__ == "__main__":
    main()