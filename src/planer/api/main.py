from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from planer.api.applications import router as applications_router

app = FastAPI(title="Bewerbungsplaner API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(applications_router)


@app.get("/")
def root():
    return {"message": "Bewerbungsplaner API"}
