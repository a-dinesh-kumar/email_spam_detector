import joblib

from src.data.preprocess import clean_text
from src.inbox.inbox import deliver_to_inbox
from src.quarantine.quarantine import quarantine_email


MODEL_PATH = "models/spam_model.pkl"
VECTORIZER_PATH = "models/count_vectorizer.pkl"


model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def classify_email(subject, body):
    """
    Classify an email and route it to
    inbox or quarantine based on prediction.
    """

    subject = subject or ""
    body = body or ""

    # Combine subject and body.
    text = subject + " " + body

    # Use the exact production preprocessing pipeline.
    cleaned_text = clean_text(text)

    # Convert cleaned text into model features.
    features = vectorizer.transform([cleaned_text])

    # Predict HAM or SPAM.
    prediction = model.predict(features)[0]

    # Route email based on prediction.
    if prediction == "spam":
        stored_email = quarantine_email(
            subject,
            body
        )

        status = "quarantined"

    else:
        stored_email = deliver_to_inbox(
            subject,
            body
        )

        status = "delivered"

    return {
        "prediction": prediction,
        "status": status,
        "email": stored_email
    }