from pathlib import Path
from datetime import datetime

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INBOX_DIR = PROJECT_ROOT / "data" / "inbox"
INBOX_FILE = INBOX_DIR / "inbox.csv"


def deliver_to_inbox(subject, body, status="ham"):
    """
    Store an email that has been delivered to the inbox.
    """

    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "id": str(datetime.now().strftime("%Y%m%d%H%M%S%f")),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "subject": subject or "",
        "body": body or "",
        "label": "ham",
        "status": status,
    }

    if INBOX_FILE.exists():
        df = pd.read_csv(
            INBOX_FILE,
            dtype={"id": str},
            keep_default_na=False
        )

        df = pd.concat(
            [df, pd.DataFrame([record])],
            ignore_index=True
        )
    else:
        df = pd.DataFrame([record])

    df.to_csv(
        INBOX_FILE,
        index=False,
        encoding="utf-8"
    )

    return record


def get_inbox_emails():
    """
    Return emails currently delivered to the inbox.
    """

    if not INBOX_FILE.exists():
        return []

    df = pd.read_csv(
        INBOX_FILE,
        dtype={"id": str},
        keep_default_na=False
    )

    if df.empty:
        return []

    return df.to_dict(orient="records")