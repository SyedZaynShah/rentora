from fastapi import FastAPI

app = FastAPI(title="Rentora API")


@app.get("/")
def root():
    return {
        "message": "Welcome to Rentora API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }