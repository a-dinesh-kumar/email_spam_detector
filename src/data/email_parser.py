from email import policy
from email.parser import BytesParser


def extract_body(message):
    """
    Extract text/plain and text/html content
    from an email message.
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


def parse_email_bytes(email_bytes):
    """
    Parse raw email bytes and return subject and body.
    """

    message = BytesParser(
        policy=policy.default
    ).parsebytes(email_bytes)

    subject = message.get("Subject", "")
    body = extract_body(message)

    return {
        "subject": subject or "",
        "body": body or "",
    }