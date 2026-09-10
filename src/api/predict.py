import joblib

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from src.data.email_parser import parse_email_bytes
from src.data.preprocess import clean_text


MODEL_PATH = "models/spam_model.pkl"
VECTORIZER_PATH = "models/count_vectorizer.pkl"


model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

router = APIRouter()


class Email(BaseModel):
    subject: str = ""
    body: str


@router.post("/predict")
def predict_email(email: Email):

    # Combine subject and body
    text = email.subject + " " + email.body

    # Apply the same preprocessing used during training
    cleaned_text = clean_text(text)

    # Convert text into model features
    features = vectorizer.transform([cleaned_text])

    # Predict
    prediction = model.predict(features)[0]

    return {
        "prediction": prediction
    }


@router.post("/predict-file")
async def predict_email_file(file: UploadFile = File(...)):

    # Accept .eml files only
    if not file.filename.lower().endswith(".eml"):
        raise HTTPException(
            status_code=400,
            detail="Only .eml files are supported."
        )

    # Read uploaded file
    email_bytes = await file.read()

    # Parse email using the shared parser
    email_data = parse_email_bytes(email_bytes)

    subject = email_data["subject"]
    body = email_data["body"]

    # Combine subject and body
    text = subject + " " + body

    # Same preprocessing as training
    cleaned_text = clean_text(text)

    # Convert to features
    features = vectorizer.transform([cleaned_text])

    # Predict
    prediction = model.predict(features)[0]

    return {
        "filename": file.filename,
        "subject": subject,
        "prediction": prediction
    }