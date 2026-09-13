import joblib

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from src.data.email_parser import parse_email_bytes
from src.utils.classifier import classify_email


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

    result = classify_email(email.subject, email.body)

    return {
        "prediction": result["prediction"],
        "status": result["status"]
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

    try:
        email_data = parse_email_bytes(email_bytes)
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to parse email file: {error}"
        )

    result = classify_email(email_data["subject"],email_data["body"])

    return {
        "filename": file.filename,
        "subject": email_data["subject"],
        "prediction": result["prediction"],
        "status": result["status"]
    }