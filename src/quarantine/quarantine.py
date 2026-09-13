from pathlib import Path
from datetime import datetime

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUARANTINE_DIR = PROJECT_ROOT / "data" / "quarantine"
QUARANTINE_FILE = QUARANTINE_DIR / "quarantine.csv"


def quarantine_email(subject, body):
    """
    Store a detected spam email in quarantine.
    """

    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "id": str(datetime.now().strftime("%Y%m%d%H%M%S%f")),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "subject": subject or "",
        "body": body or "",
        "label": "spam",
        "status": "quarantined",
    }

    if QUARANTINE_FILE.exists():
        df = pd.read_csv(
            QUARANTINE_FILE,
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
        QUARANTINE_FILE,
        index=False,
        encoding="utf-8"
    )

    return record


def get_quarantined_emails():
    """
    Return emails currently held in quarantine.
    """

    if not QUARANTINE_FILE.exists():
        return []

    df = pd.read_csv(
        QUARANTINE_FILE,
        dtype={"id": str},
        keep_default_na=False
    )

    if df.empty:
        return []

    df = df[df["status"] == "quarantined"]

    return df.to_dict(orient="records")


def release_email(email_id):
    """
    Mark a quarantined email as released.
    """

    if not QUARANTINE_FILE.exists():
        return None

    df = pd.read_csv(
        QUARANTINE_FILE,
        dtype={"id": str},
        keep_default_na=False
    )

    if df.empty:
        return None

    matches = df["id"] == str(email_id)

    if not matches.any():
        return None

    if df.loc[matches, "status"].iloc[0] != "quarantined":
        return None

    df.loc[matches, "status"] = "released"

    df.to_csv(
        QUARANTINE_FILE,
        index=False,
        encoding="utf-8"
    )

    return df.loc[matches].iloc[0].to_dict()