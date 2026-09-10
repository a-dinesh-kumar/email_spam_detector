from fastapi import FastAPI

from src.api.predict import router as predict_router


app = FastAPI(
    title="Email Spam Detection API",
    description="API for detecting whether an email is HAM or SPAM.",
    version="1.0.0"
)


app.include_router(predict_router)