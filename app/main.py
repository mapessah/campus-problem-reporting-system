from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="Campus Problem Reporting and Maintenance Management API",
)


@app.get("/")
def root():
    return {"success": True, "message": "Campus Maintenance API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
