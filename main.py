from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.predict import router as predict_router
from src.api.management import router as management_router
from src.api.overview import router as overview_router


app = FastAPI(
    title="Email Spam Detection API",
    description="API for detecting whether an email is HAM or SPAM.",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory="templates"
)


# Homepage
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


# API routers
app.include_router(predict_router)
app.include_router(management_router)
app.include_router(overview_router)