from src.data.email_parser import parse_email_bytes
from src.utils.classifier import classify_email


def main():

    sample_email = b"""\
From: marketing@example.com
To: user@example.com
Subject: Congratulations! You have won a FREE prize

Congratulations!

You have been selected to receive a FREE prize.
Click here now to claim your reward.
Limited time offer. Act immediately.
"""

    parsed_email = parse_email_bytes(sample_email)

    print("=" * 60)
    print("CLASSIFIER ROUTING TEST")
    print("=" * 60)

    print("\nSubject:", parsed_email["subject"])
    print("Body:", parsed_email["body"])

    result = classify_email(
        parsed_email["subject"],
        parsed_email["body"]
    )

    print("\nCLASSIFICATION RESULT")
    print(result)

    assert result["prediction"] in ("ham", "spam")

    if result["prediction"] == "spam":
        assert result["status"] == "quarantined"
    else:
        assert result["status"] == "delivered"

    print("\nClassifier routing test passed.")


if __name__ == "__main__":
    main()