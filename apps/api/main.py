from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router


app = FastAPI(
    title="Rentora API",
    version="0.1.0",
)


app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    users_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Rentora API",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
