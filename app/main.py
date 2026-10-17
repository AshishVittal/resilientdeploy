
import os

from fastapi import FastAPI

app = FastAPI(title="ResilientDeploy API")

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


@app.get("/")
def home():
    return {
        "application": "ResilientDeploy",
        "version": APP_VERSION,
        "message": "Application is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": APP_VERSION

    }


@app.get("/version")
def version():
    return {"version": "broken"}
