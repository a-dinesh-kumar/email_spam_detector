import re
import spacy

nlp = spacy.load("en_core_web_sm")


HEADER_PATTERN = re.compile(
    r"^(received|return-path|delivered-to|"
    r"message-id|mime-version|content-type|"
    r"content-transfer-encoding|x-[^:]+|"
    r"date|sender|reply-to|"
    r"dkim-signature|domainkey-signature):.*$",
    re.IGNORECASE
)


def remove_email_headers(text):
    lines = str(text).splitlines()

    content_lines = []

    for line in lines:
        if HEADER_PATTERN.match(line.strip()):
            continue

        content_lines.append(line)

    return "\n".join(content_lines)


def clean_text(text):
    text = remove_email_headers(text)

    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+", " ", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Keep letters and spaces
    text = re.sub(r"[^a-zA-Z ]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    doc = nlp(text)

    words = [
        token.lemma_
        for token in doc
        if not token.is_stop
    ]

    return " ".join(words)


def clean_batch(texts):
    cleaned = []

    processed_texts = [
        remove_email_headers(text)
        for text in texts
    ]

    docs = nlp.pipe(
        processed_texts,
        disable=["parser", "ner"],
        batch_size=32
    )

    for doc in docs:
        words = [
            token.lemma_
            for token in doc
            if not token.is_stop
        ]

        cleaned.append(" ".join(words))

    return cleaned