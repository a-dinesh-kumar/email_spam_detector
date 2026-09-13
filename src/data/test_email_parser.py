from src.data.email_parser import parse_email_bytes


def main():

    sample_email = b"""\
From: sender@example.com
To: receiver@example.com
Subject: Test Email

Hello, this is a test email.
Please verify the parser.
"""

    result = parse_email_bytes(sample_email)

    print("EMAIL PARSER TEST")
    print("Subject:", result["subject"])
    print("Body:", result["body"])

    assert result["subject"] == "Test Email"
    assert "Hello, this is a test email." in result["body"]

    print("\nParser test passed.")


if __name__ == "__main__":
    main()