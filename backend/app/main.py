from fastapi import FastAPI
from .database import engine, Base
from .routers import upload, results



app = FastAPI(
    title="Sports Authority of India - Talent Assessment API",
    description="API for uploading and analyzing athlete performance videos.",
    version="1.0.0"
)

app.include_router(upload.router, prefix="/api/v1", tags=["Video Upload & Processing"])
app.include_router(results.router, prefix="/api/v1", tags=["Results"])

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the SAI Talent Assessment API"}