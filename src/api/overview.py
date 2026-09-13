from fastapi import APIRouter

from src.inbox.inbox import get_inbox_emails
from src.quarantine.quarantine import get_quarantined_emails


router = APIRouter()


@router.get("/overview")
def get_overview():

    inbox_emails = get_inbox_emails()
    quarantined_emails = get_quarantined_emails()

    delivered = len(inbox_emails)
    quarantined = len(quarantined_emails)

    emails_scanned = delivered + quarantined

    if emails_scanned > 0:
        spam_rate = (quarantined / emails_scanned) * 100
    else:
        spam_rate = 0

    return {
        "emails_scanned": emails_scanned,
        "delivered": delivered,
        "quarantined": quarantined,
        "spam_rate": round(spam_rate, 2)
    }