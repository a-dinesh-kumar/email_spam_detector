from fastapi import APIRouter, HTTPException

from src.inbox.inbox import get_inbox_emails, deliver_to_inbox
from src.quarantine.quarantine import (
    get_quarantined_emails,
    release_email
)


router = APIRouter()


@router.get("/quarantine")
def get_quarantine():

    emails = get_quarantined_emails()

    return {
        "count": len(emails),
        "emails": emails
    }


@router.post("/quarantine/{email_id}/release")
def release_quarantine_email(email_id: str):

    email = release_email(email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Quarantined email not found."
        )

    # Deliver released email to inbox
    inbox_email = deliver_to_inbox(
        email["subject"],
        email["body"],
        status="released"
    )

    return {
        "message": "Email released successfully.",
        "email": inbox_email
    }


@router.get("/inbox")
def get_inbox():

    emails = get_inbox_emails()

    return {
        "count": len(emails),
        "emails": emails
    }